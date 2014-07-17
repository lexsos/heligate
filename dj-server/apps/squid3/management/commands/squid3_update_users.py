from django.core.management.base import BaseCommand

from core.log import logger
from squid3.utils import gen_excluded_users


class Command(BaseCommand):
    help = 'Generate config for squid3 excluded users'

    def handle(self, *args, **options):
        logger.info('start generate excluded users config in squid3 application')

        config = gen_excluded_users()
        self.stdout.write(config)

        logger.debug(config)
        logger.info('excluded users config successfully generated in squid3 application')
