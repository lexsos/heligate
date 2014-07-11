from accounts_web.utils import get_auth_url
from .cache import UserCache
from .models import DomainFilterKit
from .utils import extruct_domain, extruct_l2_domain, get_deny_url


def build_rules():
    groups = {}
    for filter_kit in DomainFilterKit.objects.all():
        rules = filter_kit.get_filters()
        groups[filter_kit.group.pk] = rules
    return groups


class RedirectRuls(object):

    def __init__(self):
        super(RedirectRuls, self).__init__()
        self.groups_rules = build_rules()

    def rebuild_rules(self):
        self.groups_rules = build_rules()

    def is_allowed(self, user, domain_name):

        l2_domain_name = extruct_l2_domain(domain_name)
        group_id = user.profile.group.pk

        if not group_id in self.groups_rules:
            return True

        for rule in self.groups_rules[group_id]:
            classifier, allow = rule
            if classifier.is_matched(domain_name, l2_domain_name):
                return allow

        return True


class SquidRedirector(object):

    def __init__(self, user_cache, redirect_ruls):
        super(SquidRedirector, self).__init__()
        self.user_cache = user_cache
        self.redirect_ruls = redirect_ruls

    def extruct_data(self, squid_str):
        data = squid_str.split()
        url = data[0]
        user_ip = data[1].split('/')[0]
        return url, user_ip

    def redirect(self, squid_str):
        url, user_ip = self.extruct_data(squid_str)
        user = self.user_cache.get_user_by_ip(user_ip)
        if user is None:
            auth_url = get_auth_url(url)
            return '302:{0}\n'.format(auth_url)
        domain_name = extruct_domain(url)
        if not self.redirect_ruls.is_allowed(user, domain_name):
            deny_url = get_deny_url()
            return '302:{0}\n'.format(deny_url)
        return '\n'


class Redirector(object):

    def __init__(self):
        super(Redirector, self).__init__()
        self.user_cache = UserCache(cache_miss=False)
        self.redirect_ruls = RedirectRuls()
        self.redirector = SquidRedirector(self.user_cache, self.redirect_ruls)

    def redirect(self, squid_str):
        return self.redirector.redirect(squid_str)

    def users_updated():
        self.user_cache.clear()

    def config_updated(self):
        self.user_cache.clear()
        self.redirect_ruls.rebuild_rules()
