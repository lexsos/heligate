import re

from accounts.utils import get_user_by_ip4
from .models import L2Domain, Domain, SquidLog
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


class DomainCache(object):

    def __init__(self):
        super(DomainCache, self).__init__()
        self.l1 = {}
        self.l2 = {}
        self.counter = 0
        self.max_size = DOMAIN_CACHE_SIZE
        self.period = DOMAIN_CACHE_SIZE*COUNTER_MUL
        self.miss_count = 0

    def check_cache_size(self):
        if self.counter > self.period:
            if len(self.l1) > self.max_size:
                self.l2 = self.l1
                self.l1 = {}
                self.counter = 0
        self.counter += 1

    def get_from_cache(self, dns_name):
        domain = self.l1.get(dns_name)
        if domain is None:
            domain = self.l2.get(dns_name)
            if not domain is None:
                self.l1[dns_name] = domain
        return domain

    def get_l2_domain(self, dns_name):
        l2_name = extruct_l2_domain(dns_name)
        if l2_name is None:
            return None
        else:
            l2_domain, l2_created = L2Domain.objects.get_or_create(l2_name=l2_name)
            return l2_domain

    def get_from_db(self, dns_name):
        domain, created = Domain.objects.get_or_create(name=dns_name)
        if created:
            domain.l2_domain = self.get_l2_domain(dns_name)
            domain.save()
        self.l1[dns_name] = domain
        return domain

    def get_domain(self, dns_name):
        domain = self.get_from_cache(dns_name)
        if domain is None:
            self.miss_count += 1
            domain = self.get_from_db(dns_name)
        self.check_cache_size()
        return domain


class UserCache(object):

    def __init__(self):
        super(UserCache, self).__init__()
        self.users = {}
        self.miss_count = 0

    def clear(self):
        self.users = {}
        self.miss_count = 0

    def get_user_by_ip(self, ip_address):
        user = self.users.get(ip_address, 0)
        if user == 0:
            user = get_user_by_ip4(ip_address)
            self.users[ip_address] = user
            self.miss_count += 1
        return user


class SquidLoger(object):

    def __init__(self, domain_cache, user_cache):
        super(SquidLoger, self).__init__()
        self.records = []
        self.domain_cache = domain_cache
        self.user_cache = user_cache

    def pars_squid_data(self, data):
        squid_data = data.split()
        if len(squid_data) >= 10:
            return squid_data[2], int(squid_data[4]), squid_data[6]
        return None, None

    def log(self, squid_string):

        user_ip, size, url = self.pars_squid_data(squid_string)
        if url:
            domain_name = extruct_domain(url).lower()
            if domain_name is None:
                domain_name = 'INVALID DOMAIN'
            domain = self.domain_cache.get_domain(domain_name)
            user = self.user_cache.get_user_by_ip(user_ip)
            rec = SquidLog(
                user=user,
                domain=domain,
                url=url,
                size=size,
            )
            self.records.append(rec)

    def flush(self):
        for rec in self.records:
            rec.save()
        self.records = []


class Loger(object):

    def __init__(self):
        super(Loger, self).__init__()
        self.user_cache = UserCache()
        self.domain_cache = DomainCache()
        self.squid_loger = SquidLoger(self.domain_cache, self.user_cache)

    def log(self, squid_string):
        self.squid_loger.log(squid_string)

    def flush(self):
        self.squid_loger.flush()

    def users_updated(self):
        self.user_cache.clear()
