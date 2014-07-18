import datetime
from django.core.management.base import BaseCommand

from core.log import logger
from squid3.models import SquidLog


class Command(BaseCommand):
    args = '<days>'
    help = 'Clear squid records older the <days>'

    def handle(self, *args, **options):
        if len(args) != 1:
            self.stdout.write('need <days> arg')
        days = int(args[0])
        delta = datetime.timedelta(days=days)
        date_until = datetime.datetime.today() - delta

        qs = SquidLog.objects.filter(access_date__lt=date_until)
        count = qs.count()
        qs.delete()
        msg = 'from SquidLog successfully deleted {0} records'.format(count)
        logger.info(msg)
