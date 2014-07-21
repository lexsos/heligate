from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from accounts.utils import create_account, check_profile
from .settings import CONFIG
from .auth_ldap import LdapAuthHelper
from .auth_buildin import BuildinAuthHelper


helper_classes = (LdapAuthHelper, BuildinAuthHelper)


class AuthHelper(object):

    def __init__(self):
        super(AuthHelper, self).__init__()
        self.auth_helpers = []

        for helper_class in helper_classes:
            helper = helper_class(CONFIG)
            self.auth_helpers.append(helper)

    def auth(self, user_name, password):
        for helper in self.auth_helpers:
            if helper.auth(user_name, password):
                return True
        return False

    def get_user_info(self, user_name, password):
        for helper in self.auth_helpers:
            info = helper.get_user_info(user_name, password)
            if not info is None:
                return info
        return None

    def get_or_create_user(self, user_info):
        try:
            user = User.objects.get(username=user_info['user_name'])
            check_profile(
                user_info['user_name'],
                CONFIG['DEFAULT_IP4'],
                CONFIG['DEFAULT_GROUP'],
                user_info['full_name'],
            )
            return user
        except ObjectDoesNotExist:
            return create_account(
                user_info['user_name'],
                CONFIG['DEFAULT_IP4'],
                CONFIG['DEFAULT_GROUP'],
                user_info['full_name'],
            )

    def get_user(self, user_name, password):
        if not self.auth(user_name, password):
            return None
        info = self.get_user_info(user_name, password)
        return self.get_or_create_user(info)
