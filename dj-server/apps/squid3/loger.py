import re

from accounts.utils import get_user_by_ip4
from .models import Domain, SquidLog


re_url = re.compile(r'^https?://(?P<domain>[^ \f\n\r\t\v/]+)')


def extruct_domain(url):
    m = re_url.search(url)
    if m is None:
        return None
    return m.group('domain')


class SquidLoger(object):

    def pars_squid_data(self, data):
        squid_data = data.split()
        if len(squid_data) >= 10:
            return squid_data[2] ,int(squid_data[4]), squid_data[6]
        return None, None

    def get_domain(self, domain_name):
        domain, created = Domain.objects.get_or_create(dns=domain_name)
        return domain

    def log(self, squid_string):

        user_ip, size, url = self.pars_squid_data(squid_string)
        if url:
            domain_name = extruct_domain(url).lower()
            domain = self.get_domain(domain_name)
            user = get_user_by_ip4(user_ip)
            rec = SquidLog(
                user=user,
                domain=domain,
                url=url,
                size=size,
            )
            rec.save()

    def flush(self):
        pass
