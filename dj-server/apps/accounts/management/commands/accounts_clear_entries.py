from django.core.management.base import BaseCommand

from accounts.models import Ip4Entry


class Command(BaseCommand):
    help = 'Delete all IP entries'

    def handle(self, *args, **options):

        Ip4Entry.objects.all().delete()
        self.stdout.write('All IP entries successfully deleted')
