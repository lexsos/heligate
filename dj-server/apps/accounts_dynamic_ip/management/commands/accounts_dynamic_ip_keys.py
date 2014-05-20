import os
import json

from django.core.management.base import BaseCommand

from accounts_dynamic_ip.models import DynamicAccounts


def save_key(dyn_account, dir_path):
    user_name = dyn_account.user.username
    file_name = os.path.join(dir_path, user_name)
    f = open(file_name, 'w')
    data = {
        'user': user_name,
        'secret': dyn_account.secret,
    }
    f.write(json.dumps(data))
    f.close()


class Command(BaseCommand):
    help = 'Generate key file for users'
    args = 'dir_path [user_name]'

    def handle(self, *args, **options):
        if len(args) < 1:
            self.stdout.write(u'Need dir_path parametr')
            return
        elif len(args) == 1:
            dir_path = args[0]
            for dyn_account in DynamicAccounts.objects.all():
                save_key(dyn_account, dir_path)
        else:
            dir_path = args[0]
            for user_name in args[1:]:
                dyn_account = DynamicAccounts.objects.get(
                    user__username=user_name
                )
                save_key(dyn_account, dir_path)
