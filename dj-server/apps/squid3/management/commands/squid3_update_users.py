from django.core.management.base import BaseCommand

from squid3.utils import gen_excluded_users


class Command(BaseCommand):
    help = 'Generate config for squid3 excluded users'

    def handle(self, *args, **options):
         self.stdout.write(gen_excluded_users())
