from django import forms
from django.utils.translation import ugettext_lazy as _

from .auth import AuthHelper


class WebAuthForm(forms.Form):

    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    auth_helper = AuthHelper()

    def clean(self):
        cleaned_data = super(WebAuthForm, self).clean()
        user_name = cleaned_data.get('user_name')
        password = cleaned_data.get('password')

        user = self.auth_helper.get_user(user_name, password)
        if user is None:
            raise forms.ValidationError(_('user\password invalid'))

        cleaned_data['user'] = user
        return cleaned_data
