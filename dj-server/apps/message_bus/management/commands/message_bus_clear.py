from django.core.management.base import BaseCommand

from message_bus.models import Event


class Command(BaseCommand):
    help = 'Delete all event log entries'

    def handle(self, *args, **options):

        Event.objects.all().delete()
        self.stdout.write('All event log entries successfully deleted')