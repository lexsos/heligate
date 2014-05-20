from django.core.management.base import BaseCommand

from firewall.utils import get_all_conf


class Command(BaseCommand):
    help = 'Generate config for firewall'

    def handle(self, *args, **options):
        self.stdout.write(get_all_conf())
