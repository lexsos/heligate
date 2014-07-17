import datetime

from core.log import logger

from .models import SquidLog
from .cache import UserCache, DomainCache
from .utils import extruct_domain


class SquidLogger(object):

    def __init__(self, domain_cache, user_cache):
        super(SquidLogger, self).__init__()
        self.records = []
        self.domain_cache = domain_cache
        self.user_cache = user_cache

    def pars_squid_data(self, data):
        squid_data = data.split()
        if len(squid_data) >= 10:
            return squid_data[2], int(squid_data[4]), squid_data[6]
        return None, None, None

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


class Logger(object):

    def __init__(self):
        super(Logger, self).__init__()
        self.user_cache = UserCache()
        self.domain_cache = DomainCache()
        self.squid_logger = SquidLogger(self.domain_cache, self.user_cache)
        self.record_count = 0
        self.profiler_time = datetime.timedelta()

    def log(self, squid_string):
        start = datetime.datetime.now()
        self.squid_logger.log(squid_string)
        self.profiler_time += datetime.datetime.now() - start
        self.record_count += 1

    def flush(self):
        start = datetime.datetime.now()
        self.squid_logger.flush()
        self.profiler_time += datetime.datetime.now() - start

    def users_updated(self):
        self.log_statistic()
        self.user_cache.clear()

    def config_updated(self):
        self.log_statistic()
        self.user_cache.clear()
        self.domain_cache.clear()

    def log_statistic(self):
        self.user_cache.log_statistic()
        self.domain_cache.log_statistic()

        msg = 'squid3 logger processed {0} records in {1} time'
        msg = msg.format(self.record_count, self.profiler_time)
        logger.debug(msg)
