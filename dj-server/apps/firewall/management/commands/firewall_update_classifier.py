from django.core.management.base import BaseCommand

from core.log import logger
from firewall.utils import get_update_classifier


class Command(BaseCommand):
    help = 'Generate sh script for update classifier chain'

    def handle(self, *args, **options):
        logger.info('start generate user classifier in firewall application')

        config = get_update_classifier()
        self.stdout.write(config)

        logger.debug(config)
        logger.info('user classifier successfully generated  in firewall application')
