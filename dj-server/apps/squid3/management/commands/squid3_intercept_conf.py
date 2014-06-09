from django.core.management.base import BaseCommand

from squid3.utils import gen_intercept_conf


class Command(BaseCommand):
    help = 'Generate config for squid3 interception'

    def handle(self, *args, **options):
         self.stdout.write(gen_intercept_conf())
