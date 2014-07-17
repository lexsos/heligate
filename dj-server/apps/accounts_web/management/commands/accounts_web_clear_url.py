from django.core.management.base import BaseCommand

from core.log import logger
from accounts_web.models import RedirectUrl


class Command(BaseCommand):
    help = 'Delete all URL entries'

    def handle(self, *args, **options):

        logger.info('start clear URL entries in accounts_web application')
        RedirectUrl.objects.all().delete()
        logger.info('all URL entries successfully deleted in accounts_web application')
