from django.core.management.base import BaseCommand

from core.log import logger
from message_bus.models import Event


class Command(BaseCommand):
    help = 'Delete all event log entries'

    def handle(self, *args, **options):

        logger.info('start clear events entries in message_bus application')
        Event.objects.all().delete()
        logger.info('all events entries successfully deleted in message_bus application')
