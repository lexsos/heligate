import datetime
from django.core.management.base import BaseCommand

from core.log import logger
from core.utils import has_related_objects, console_progrees
from squid3.models import L2Domain, Domain


class Command(BaseCommand):
    help = 'Clear unused domains'

    def clear_model(self, model):
        self.stdout.write('start clearing {0}'.format(model.__name__))
        qs = model.objects.all()
        del_count = 0
        total_count = qs.count()

        for (counter, record)  in enumerate(qs):
            console_progrees(total_count, counter + 1, self.stdout)
            if has_related_objects(record):
                continue
            record.delete()
            del_count += 1

        self.stdout.write('')
        msg = 'from {0} successfully deleted {1} records'.format(
            model.__name__,
            del_count,
        )
        logger.info(msg)

    def handle(self, *args, **options):
        self.clear_model(Domain)
        self.clear_model(L2Domain)

