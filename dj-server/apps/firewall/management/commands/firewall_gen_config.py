from django.core.management.base import BaseCommand

from core.log import logger
from firewall.utils import get_all_conf


class Command(BaseCommand):
    help = 'Generate config for firewall'

    def handle(self, *args, **options):
        logger.debug('start generate config for iptables in firewall application')

        config = get_all_conf()
        self.stdout.write(config)

        logger.debug(config)
        logger.debug('config successfully generated for iptables in firewall application')
