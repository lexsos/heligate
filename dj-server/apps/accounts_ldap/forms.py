from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from accounts.utils import create_account
from .utils import get_user_info
from .settings import CONFIG


class LdapAuthForm(forms.Form):

    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def get_or_create_user(self, user_info):
        try:
            user = User.objects.get(username=user_info['user_name'])
            return user
        except ObjectDoesNotExist:
            if not CONFIG['INET_GROPUT'] in user_info['groups']:
                raise forms.ValidationError(_('access denied'))
            return create_account(
                user_info['user_name'],
                CONFIG['DEFAULT_IP4'],
                CONFIG['DEFAULT_GROUP'],
                user_info['full_name'],
            )

    def clean(self):
        cleaned_data = super(LdapAuthForm, self).clean()
        user_name = cleaned_data.get('user_name')
        password = cleaned_data.get('password')

        user_info = get_user_info(
            CONFIG['LDAP_DOMAIN'],
            CONFIG['LDAP_TREE'],
            user_name,
            password,
        )
        if user_info is None:
            raise forms.ValidationError(_('user\password invalid'))
        cleaned_data['user'] = self.get_or_create_user(user_info)
        return cleaned_data
