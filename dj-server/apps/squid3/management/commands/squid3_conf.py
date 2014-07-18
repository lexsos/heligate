from django.core.management.base import BaseCommand

from core.log import logger
from squid3.utils import gen_squid_conf
from squid3.settings import CONFIG


class Command(BaseCommand):
    help = 'Generate config for squid3 daemon'

    def handle(self, *args, **options):
        logger.debug('start generating config for squid3 daemon in squid3 application')

        config = gen_squid_conf()
        logger.debug(config)

        conf_file_name = CONFIG['SQUID_CONF_FILE']
        try:
            f = open(conf_file_name, 'w')
            f.write(config)
            f.close()
        except IOError:
            msg = "can't write file {0}".format(conf_file_name)
            logger.error(msg)
        else:
            logger.debug('config for squid3 daemon successfully generated in squid3 application')
