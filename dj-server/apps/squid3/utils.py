from django.template.loader import render_to_string

from core.utils import normalize_script
from firewall.settings import CONFIG
from accounts.utils import get_ip4_list
from .models import (
    ExcludedFilter,
    ExcludedUser,
    InterceptFilter,
)


def gen_intercept_conf():

    context = {
        'excluded_filter_list': ExcludedFilter.objects.filter(enabled=True),
        'intercept_filter_list': InterceptFilter.objects.filter(enabled=True),
        'mark': CONFIG['DIVERT_MARK'],
    }
    conf = render_to_string('squid3/intercept_conf.sh', context)
    return normalize_script(conf)


def gen_excluded_users():
    ip4_list = set()
    for excluded_user in ExcludedUser.objects.all():
        ip4_list |= set(get_ip4_list(excluded_user.user))

    context = {
        'ip4_list': ip4_list,
    }
    conf = render_to_string('squid3/excluded_users.sh', context)
    return normalize_script(conf)
