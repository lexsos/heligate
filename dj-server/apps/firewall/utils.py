import re

from django.template.loader import render_to_string
from django.contrib.auth.models import Group


def get_ipt_params(classifier):
    result = u''
    if classifier.protocol:
        result += u'-p ' + classifier.protocol + u' '
    if classifier.src_ip:
        result += u'-src ' + classifier.src_ip + u' '
    if classifier.dst_ip:
        result += u'-dst ' + classifier.dst_ip + u' '
    if classifier.input_if:
        result += u'-i ' + classifier.input_if.name + u' '
    if classifier.output_if:
        result += u'-o ' + classifier.output_if.name + u' '
    if classifier.src_ports:
        result += u'-m multiport --sports ' + classifier.src_ports + u' '
    if classifier.dst_ports:
        result += u'-m multiport --dports ' + classifier.dst_ports + u' '
    if classifier.icmp_type:
        result += u'--icmp-type ' + classifier.icmp_type + u' '
    return result


def normalize_script(script):
    norma = script
    norma= re.sub(u' +', u' ', norma)
    norma= re.sub(u'\n\s*', u'\n', norma)
    norma= re.sub(u'^\s*\n', u'', norma)
    return norma


def get_all_conf():
        context = {
            'group_list': Group.objects.all(),
        }
        conf = render_to_string('firewall/config.sh', context)
        return normalize_script(conf)
