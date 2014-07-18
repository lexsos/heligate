from django.core.management.base import BaseCommand

from core.log import logger
from squid3.utils import gen_squid_conf
from squid3.settings import CONFIG


class Command(BaseCommand):
    help = 'Generate config for squid3 daemon'

    def handle(self, *args, **options):
        logger.debug('start generating config for squid3 daemon in squid3 application')

        config = gen_squid_conf()
        f = open(CONFIG['SQUID_CONF_FILE'], 'w')
        f.write(config)
        f.close()

        logger.debug(config)
        logger.debug('config for squid3 daemon successfully generated in squid3 application')
