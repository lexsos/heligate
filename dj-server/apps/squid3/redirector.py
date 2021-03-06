import datetime

from core.log import logger
from accounts_web.utils import get_auth_url

from .cache import UserCache, DomainCache, DomainFilterCache
from .utils import (
    extruct_domain,
    get_deny_url,
    build_rules,
)


class DomainAccessRules(object):

    def __init__(self, filter_cache, default_allow=True):
        super(DomainAccessRules, self).__init__()
        self.groups_rules = build_rules()
        self.default = default_allow
        self.filter_cache = filter_cache

    def rebuild_rules(self):
        self.groups_rules = build_rules()

    def is_allowed(self, user, domain):

        allowed = self.filter_cache.get(user, domain)
        if not allowed is None:
            return allowed

        group_id = user.profile.group.pk

        if not group_id in self.groups_rules:
            return self.default

        for rule in self.groups_rules[group_id]:
            classifier, allow = rule
            if classifier.is_matched(domain):
                self.filter_cache.add(user, domain, allow)
                return allow

        return self.default


class SquidRedirector(object):

    def __init__(self, user_cache, redirect_rules, domain_cache):
        super(SquidRedirector, self).__init__()
        self.user_cache = user_cache
        self.redirect_rules = redirect_rules
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

        if not self.redirect_rules.is_allowed(user, domain):
            deny_url = get_deny_url()
            return self.get_redirection(deny_url)

        return '\n'


class Redirector(object):

    def __init__(self):
        super(Redirector, self).__init__()
        self.user_cache = UserCache(cache_miss=False)
        self.domain_cache = DomainCache()
        self.domain_filter_cache = DomainFilterCache()
        self.redirect_rules = DomainAccessRules(self.domain_filter_cache)

        self.redirector = SquidRedirector(
            self.user_cache,
            self.redirect_rules,
            self.domain_cache,
        )

        self.record_count = 0
        self.profiler_time = datetime.timedelta()

    def redirect(self, squid_str):
        start = datetime.datetime.now()
        url = self.redirector.redirect(squid_str)
        self.profiler_time += datetime.datetime.now() - start
        self.record_count += 1
        return url

    def users_updated(self):
        self.log_statistic()
        self.user_cache.clear()

    def config_updated(self):
        self.log_statistic()
        self.user_cache.clear()
        self.domain_cache.clear()
        self.domain_filter_cache.clear()
        self.redirect_rules.rebuild_rules()

    def log_statistic(self):
        self.user_cache.log_statistic()
        self.domain_cache.log_statistic()
        self.domain_filter_cache.log_statistic()

        msg = 'rederector processed {0} queries in {1} time'
        msg = msg.format(self.record_count, self.profiler_time)
        logger.debug(msg)
