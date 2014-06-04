import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse

from accounts.utils import user_reg_ip4
from event_log.utils import apply_events
from event_log.patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
)

from .models import DynamicAccounts
from .settings import CONFIG


class AuthView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AuthView, self).dispatch(*args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def read_json_data(self):
        try:
            self.json_data = json.loads(self.request.body)
            return 0
        except ValueError:
            return 1

    def get_response(self, data):
        return HttpResponse(json.dumps(data))

    def response_msg(self, status, msg):
        return self.get_response(
            {
                'status': status,
                'descriptions': msg,
            }
        )

    def response_err(self, msg):
        return self.response_msg('error', msg)

    def response_suc(self, msg):
        return self.response_msg('success', msg)

    def post(self, request, *args, **kwargs):
        if self.read_json_data() != 0:
            return self.response_err('need proper json data')
        if not ('user' in self.json_data) or not ('secret' in self.json_data):
            return self.response_err('need user and secret values')

        accounts = DynamicAccounts.objects.filter(
            user__username=self.json_data['user'],
            secret=self.json_data['secret'],
        )
        if not accounts.exists():
            return self.response_err('user not fount or wrong secret')

        user = accounts[0].user
        ip_address = self.get_client_ip()
        if user_reg_ip4(user, ip_address, CONFIG['PRIORITY']) != 0:
            return self.response_err("can't register user")

        msg = 'user {0} with ip {1} registred'.format(
            user.username,
            ip_address,
        )
        apply_events([ACCOUNTS_REG_USER, ACCOUNTS_UNREG_USER])
        return self.response_suc(msg)
