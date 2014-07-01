from django.core.management.base import BaseCommand

from accounts_ldap.models import RedirectUrl


class Command(BaseCommand):
    help = 'Delete all URL entries'

    def handle(self, *args, **options):

        RedirectUrl.objects.all().delete()
        self.stdout.write('All URL entries successfully deleted')
