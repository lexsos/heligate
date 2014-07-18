from django.core.management.base import BaseCommand

from core.log import logger
from accounts.models import Ip4Entry


class Command(BaseCommand):
    help = 'Delete all IP entries'

    def handle(self, *args, **options):

        logger.debug('start clear IP entries in accounts application')
        Ip4Entry.objects.all().delete()
        logger.debug('all IP entries successfully deleted in accounts application')
