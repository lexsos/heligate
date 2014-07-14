from accounts_web.utils import get_auth_url
from .cache import UserCache, DomainCache
from .utils import (
    extruct_domain,
    get_deny_url,
    build_rules,
)


class DomainAccessRules(object):

    def __init__(self, default_allow=True):
        super(DomainAccessRules, self).__init__()
        self.groups_rules = build_rules()
        self.default = default_allow

    def rebuild_rules(self):
        self.groups_rules = build_rules()

    def is_allowed(self, user, domain):

        group_id = user.profile.group.pk

        if not group_id in self.groups_rules:
            return self.default

        for rule in self.groups_rules[group_id]:
            classifier, allow = rule
            if classifier.is_matched(domain):
                return allow

        return self.default


class SquidRedirector(object):

    def __init__(self, user_cache, redirect_ruls, domain_cache):
        super(SquidRedirector, self).__init__()
        self.user_cache = user_cache
        self.redirect_ruls = redirect_ruls
        self.domain_cache = domain_cache

    def extruct_data(self, squid_str):
        data = squid_str.split()
        url = data[0]
        user_ip = data[1].split('/')[0]
        return url, user_ip

    def get_redirection(self, url):
        return '302:{0}\n'.format(url)

    def redirect(self, squid_str):
        url, user_ip = self.extruct_data(squid_str)
        user = self.user_cache.get_user_by_ip(user_ip)
        domain_name = extruct_domain(url)
        if domain_name is None:
            domain_name = 'INVALID DOMAIN'
        domain = self.domain_cache.get_domain(domain_name)

        if user is None:
            auth_url = get_auth_url(url)
            return self.get_redirection(auth_url)

        if not self.redirect_ruls.is_allowed(user, domain):
            deny_url = get_deny_url()
            return self.get_redirection(deny_url)

        return '\n'


class Redirector(object):

    def __init__(self):
        super(Redirector, self).__init__()
        self.user_cache = UserCache(cache_miss=False)
        self.domain_cache = DomainCache()
        self.redirect_ruls = DomainAccessRules()
        self.redirector = SquidRedirector(
            self.user_cache,
            self.redirect_ruls,
            self.domain_cache,
        )

    def redirect(self, squid_str):
        return self.redirector.redirect(squid_str)

    def users_updated(self):
        self.user_cache.clear()

    def config_updated(self):
        self.user_cache.clear()
        self.domain_cache.clear()
        self.redirect_ruls.rebuild_rules()
