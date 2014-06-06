import re

from django.template.loader import render_to_string
from django.contrib.auth.models import Group

from .settings import CONFIG
from .patterns import INTERNAL_IF


def get_ipt_params(classifier):
    result = u''

    if classifier.protocol:
        result += u'-p ' + classifier.protocol + u' '

    if classifier.src_ip:
        if classifier.src_ip_not:
            result += u'! '
        result += u'--src ' + classifier.src_ip + u' '

    if classifier.dst_ip:
        if classifier.dst_ip_not:
            result += u'! '
        result += u'--dst ' + classifier.dst_ip + u' '

    if classifier.input_if:
        if classifier.input_if_not:
            result += u'! '
        result += u'-i ' + classifier.input_if.if_name + u' '

    if classifier.output_if:
        if classifier.output_if_not:
            result += u'! '
        result += u'-o ' + classifier.output_if.if_name + u' '

    if classifier.src_ports:
        result += u'-m multiport '
        if classifier.src_ports_not:
            result += u'! '
        result += u'--sports ' + classifier.src_ports + u' '

    if classifier.dst_ports:
        result += u'-m multiport '
        if classifier.dst_ports_not:
            result += u'! '
        result += u'--dports ' + classifier.dst_ports + u' '

    if classifier.icmp_type:
        result += u'--icmp-type ' + classifier.icmp_type + u' '
    return result


def normalize_script(script):
    norma = script
    norma = re.sub(u' +', u' ', norma)
    norma = re.sub(u'\n\s*', u'\n', norma)
    norma = re.sub(u'^\s*\n', u'', norma)
    return norma


def get_all_conf():
    from .models import NetInterface
    internal_if = NetInterface.objects.filter(if_type=INTERNAL_IF)[0]
    internal_if = internal_if.if_name
    context = {
        'group_list': Group.objects.all(),
        'divert_mark': CONFIG['DIVERT_MARK'],
        'divert_route_table': CONFIG['DIVERT_ROUTE_TABLE'],
        'internal_if': internal_if,
    }
    conf = render_to_string('firewall/config.sh', context)
    return normalize_script(conf)


def get_update_classifier():
    conf = render_to_string('firewall/update_classifier.sh')
    return normalize_script(conf)
