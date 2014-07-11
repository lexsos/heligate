from .models import SquidLog
from .cache import UserCache, DomainCache
from .utils import extruct_domain


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
            domain_name = extruct_domain(url)
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

    def config_updated(self):
        self.user_cache.clear()
        self.domain_cache.clear()
