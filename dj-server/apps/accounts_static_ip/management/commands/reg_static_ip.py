from django.core.management.base import BaseCommand

from core.log import logger
from accounts_static_ip.models import StaticIp4


class Command(BaseCommand):
    help = 'Register static ip'

    def handle(self, *args, **options):

        logger.debug('start register IP in accounts_static_ip application')

        count = 0
        for static_ip in StaticIp4.objects.all():
            static_ip.register()
            count += 1

        msg = 'static ip[{0}] successfully registered in ' \
            'accounts_static_ip application'
        msg = msg.format(count)
        logger.debug(msg)
