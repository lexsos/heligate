import re

from accounts.utils import get_user_by_ip4
from .models import Domain, SquidLog
from .settings import CONFIG


DOMAIN_CACHE_SIZE = CONFIG['DOMAIN_CACHE_SIZE']
COUNTER_MUL = CONFIG['COUNTER_MUL']
re_url = re.compile(r'^https?://(?P<domain>[^ \f\n\r\t\v/:]+)')
re_l2_domain = re.compile(r'^([^ \f\n\r\t\v/:]+\.)*(?P<l2_domain>[^ \.\f\n\r\t\v/:]+\.[^ \.\f\n\r\t\v/:]+)$')


def extruct_domain(url):
    m = re_url.search(url)
    if m is None:
        return None
    return m.group('domain')


def extruct_l2_domain(domain_name):
    m = re_l2_domain.search(domain_name)
    if m is None:
        return None
    return m.group('l2_domain')


class SquidLoger(object):

    def __init__(self):
        super(SquidLoger, self).__init__()
        self.domains_l1 = {}
        self.domains_l2 = {}
        self.domains_counter = 0
        self.users = {}
        self.records = []

    def get_user(self, ip_address):
        user = self.users.get(ip_address, 0)
        if user == 0:
            user = get_user_by_ip4(ip_address)
            self.users[ip_address] = user

        return user

    def clear_user_cache(self):
        self.users = {}

    def get_domain(self, domain_name):

        domain = self.domains_l1.get(domain_name)

        if domain is None:
            domain = self.domains_l2.get(domain_name)
            if not domain is None:
                self.domains_l1[domain_name] = domain

        if domain is None:
            domain, created = Domain.objects.get_or_create(dns=domain_name)
            self.domains_l1[domain_name] = domain

        if self.domains_counter > DOMAIN_CACHE_SIZE*COUNTER_MUL:
            if len(self.domains_l1) > DOMAIN_CACHE_SIZE:
                self.domains_l2 = self.domains_l1
                self.domains_l1 = {}
                self.domains_counter = 0

        self.domains_counter += 1
        return domain

    def pars_squid_data(self, data):
        squid_data = data.split()
        if len(squid_data) >= 10:
            return squid_data[2] ,int(squid_data[4]), squid_data[6]
        return None, None

    def log(self, squid_string):

        user_ip, size, url = self.pars_squid_data(squid_string)
        if url:
            domain_name = extruct_domain(url).lower()
            if domain_name is None:
                domain_name = 'INVALID DOMAIN'
            domain = self.get_domain(domain_name)
            user = self.get_user(user_ip)
            rec = SquidLog(
                user=user,
                domain=domain,
                url=url,
                size=size,
            )
            self.records.append(rec)

    def flush(self):
        for rec in  self.records:
            rec.save()
        self.records = []
