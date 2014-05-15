from django.core.management.base import BaseCommand

from accounts_static_ip.models import StaticIp4


class Command(BaseCommand):
    help = 'Register static ip'

    def handle(self, *args, **options):

        for static_ip in StaticIp4.objects.all():
            static_ip.register()
        self.stdout.write('Static ip successfully registered')
