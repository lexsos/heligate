from accounts.utils import get_user_by_ip4
from .models import L2Domain, Domain
from .settings import CONFIG
from .utils import extruct_l2_domain
from core.log import logger


DOMAIN_CACHE_SIZE = CONFIG['DOMAIN_CACHE_SIZE']
FILTER_CACHE_SIZE = CONFIG['FILTER_CACHE_SIZE']
COUNTER_MUL = CONFIG['COUNTER_MUL']


class UserCache(object):

    def __init__(self, cache_miss=True):
        super(UserCache, self).__init__()
        self.cache_l1 = {}
        self.miss_count = 0
        self.query_count = 0
        self.cache_miss = cache_miss

    def log_statistic(self):
        format_str = \
            'UserCache statistic [query count]:{0} ' \
            '[miss count]:{1} [cache size]:{2}'
        msg = format_str.format(
            self.query_count,
            self.miss_count,
            len(self.cache_l1),
        )
        logger.debug(msg)

    def clear(self):
        self.cache_l1 = {}
        self.miss_count = 0
        self.query_count = 0

    def get_user_by_ip(self, ip_address):
        self.query_count += 1
        user = self.cache_l1.get(ip_address, 0)
        if user == 0:
            self.miss_count += 1
            user = get_user_by_ip4(ip_address)
            if (not user is None) or self.cache_miss:
                self.cache_l1[ip_address] = user
        return user


class DomainCache(object):

    def __init__(self):
        super(DomainCache, self).__init__()
        self.cache_l1 = {}
        self.cache_l2 = {}
        self.query_count = 0
        self.max_size = DOMAIN_CACHE_SIZE
        self.period = DOMAIN_CACHE_SIZE*COUNTER_MUL
        self.miss_count = 0

    def log_statistic(self):
        format_str = \
            'DomainCache statistic [query count]:{0} [miss count]:{1} ' \
            '[L1 cache size]:{2} [L2 cache size]:{3}'
        msg = format_str.format(
            self.query_count,
            self.miss_count,
            len(self.cache_l1),
            len(self.cache_l2),
        )
        logger.debug(msg)

    def clear(self):
        self.cache_l1 = {}
        self.cache_l2 = {}
        self.query_count = 0
        self.miss_count = 0

    def check_cache_size(self):
        if self.query_count > self.period:
            if len(self.cache_l1) > self.max_size:
                self.cache_l2 = self.cache_l1
                self.cache_l1 = {}
                self.query_count = 0
        self.query_count += 1

    def get_from_cache(self, dns_name):
        domain = self.cache_l1.get(dns_name)
        if domain is None:
            domain = self.cache_l2.get(dns_name)
            if not domain is None:
                self.cache_l1[dns_name] = domain
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
        self.cache_l1[dns_name] = domain
        return domain

    def get_domain(self, dns_name):
        domain = self.get_from_cache(dns_name)
        if domain is None:
            self.miss_count += 1
            domain = self.get_from_db(dns_name)
        self.check_cache_size()
        return domain


class DomainFilterCache(object):

    def __init__(self):
        super(DomainFilterCache, self).__init__()
        self.cache_l1 = {}
        self.cache_l2 = {}
        self.cache_size = 0
        self.miss_count = 0
        self.query_count = 0

    def log_statistic(self):
        format_str = \
            'DomainFilterCache statistic [query count]:{0} ' \
            '[miss count]:{1} [cache size]:{2}'
        msg = format_str.format(
            self.query_count,
            self.miss_count,
            self.cache_size,
        )
        logger.debug(msg)

    def clear(self):
        self.miss_count = 0
        self.cache_size = 0
        self.query_count = 0
        self.cache_l2 = {}
        self.cache_l1 = {}

    def check_cache_size(self):
        self.cache_size += 1
        if self.cache_size > FILTER_CACHE_SIZE:
            cache = self.cache_l1
            self.clear()
            self.cache_l2 = cache

    def get(self, user, domain):
        self.query_count += 1

        if user.pk in self.cache_l1:
            user_rules = self.cache_l1[user.pk]
            if domain.pk in user_rules:
                return user_rules[domain.pk]

        if user.pk in self.cache_l2:
            user_rules = self.cache_l2[user.pk]
            if domain.pk in user_rules:
                allowed = user_rules[domain.pk]
                self.add(user, domain, allowed)
                return allowed

        self.miss_count += 1
        return None

    def add(self, user, domain, access_allow):
        if not user.pk in self.cache_l1:
            self.cache_l1[user.pk] = {}

        user_rules = self.cache_l1[user.pk]
        user_rules[domain.pk] = access_allow
        self.check_cache_size()
