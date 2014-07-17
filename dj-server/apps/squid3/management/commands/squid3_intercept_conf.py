from django.core.management.base import BaseCommand

from core.log import logger
from squid3.utils import gen_intercept_conf


class Command(BaseCommand):
    help = 'Generate config for squid3 interception'

    def handle(self, *args, **options):
        logger.info('start generate intercept config in squid3 application')

        config = gen_intercept_conf()
        self.stdout.write(config)

        logger.debug(config)
        logger.info('intercept config successfully generated  in squid3 application')
