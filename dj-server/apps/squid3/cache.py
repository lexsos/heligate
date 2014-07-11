from accounts.utils import get_user_by_ip4
from .models import L2Domain, Domain
from .settings import CONFIG
from .utils import extruct_l2_domain


DOMAIN_CACHE_SIZE = CONFIG['DOMAIN_CACHE_SIZE']
COUNTER_MUL = CONFIG['COUNTER_MUL']


class UserCache(object):

    def __init__(self, cache_miss=True):
        super(UserCache, self).__init__()
        self.users = {}
        self.miss_count = 0
        self.cache_miss = cache_miss

    def clear(self):
        self.users = {}
        self.miss_count = 0

    def get_user_by_ip(self, ip_address):
        user = self.users.get(ip_address, 0)
        if user == 0:
            self.miss_count += 1
            user = get_user_by_ip4(ip_address)
            if (not user is None) or self.cache_miss:
                self.users[ip_address] = user
        return user


class DomainCache(object):

    def __init__(self):
        super(DomainCache, self).__init__()
        self.l1 = {}
        self.l2 = {}
        self.counter = 0
        self.max_size = DOMAIN_CACHE_SIZE
        self.period = DOMAIN_CACHE_SIZE*COUNTER_MUL
        self.miss_count = 0

    def clear(self):
        self.l1 = {}
        self.l2 = {}
        self.counter = 0
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
