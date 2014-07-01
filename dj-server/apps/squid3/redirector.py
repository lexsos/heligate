from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from .loger import UserCache


def get_auth_url():
    site = Site.objects.get_current()
    url = reverse('accounts_ldap_auth')
    return 'http://{0}{1}'.format(site, url)


class SquidRedirector(object):

    def __init__(self, user_cache):
        super(SquidRedirector, self).__init__()
        self.user_cache = user_cache

    def extruct_data(self, squid_str):
        data = squid_str.split()
        url = data[0]
        user_ip = data[1].split('/')[0]
        return url, user_ip

    def redirect(self, squid_str):
        url, user_ip = self.extruct_data(squid_str)
        user = self.user_cache.get_user_by_ip(user_ip)
        if user is None:
            auth_url = get_auth_url()
            return '302:{0}\n'.format(auth_url)
        return '\n'


class Redirector(object):

    def __init__(self):
        super(Redirector, self).__init__()
        self.user_cache = UserCache()
        self.redirector = SquidRedirector(self.user_cache)

    def redirect(self, squid_str):
        return self.redirector.redirect(squid_str)
