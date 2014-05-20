from django.core.management.base import BaseCommand

from firewall.utils import get_update_classifier


class Command(BaseCommand):
    help = 'Generate sh script for update classifier chain'

    def handle(self, *args, **options):
        self.stdout.write(get_update_classifier())
