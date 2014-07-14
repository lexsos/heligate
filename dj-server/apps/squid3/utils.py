import re
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from core.utils import normalize_script
from firewall.settings import CONFIG
from accounts.utils import get_ip4_list
from .models import (
    ExcludedFilter,
    ExcludedUser,
    InterceptFilter,
    DomainFilterKit,
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


re_url = re.compile(r'^https?://(?P<domain>[^ \f\n\r\t\v/:]+)')


def extruct_domain(url):
    m = re_url.search(url)
    if m is None:
        return None
    return m.group('domain').lower()


re_l2_domain = re.compile(r'^([^ \f\n\r\t\v/:]+\.)*(?P<l2_domain>[^ \.\f\n\r\t\v/:]+\.[^ \.\f\n\r\t\v/:]+)$')


def extruct_l2_domain(domain_name):
    m = re_l2_domain.search(domain_name)
    if m is None:
        return None
    return m.group('l2_domain')


def get_deny_url():
    uri = reverse('squi3_deny')
    site = Site.objects.get_current()
    return 'http://{0}{1}'.format(site, uri)


def build_rules():
    groups = {}
    for filter_kit in DomainFilterKit.objects.all():
        rules = filter_kit.get_filters()
        groups[filter_kit.group.pk] = rules
    return groups
