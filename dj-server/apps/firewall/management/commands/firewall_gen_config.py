from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Generate config for firewall'

    def handle(self, *args, **options):
        context = {
            'group_list': Group.objects.all(),
        }
        conf = render_to_string('firewall/config.sh', context)
        self.stdout.write(conf)
