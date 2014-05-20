from __future__ import absolute_import

from django.template import Library

from accounts.models import Ip4Entry


register = Library()


@register.inclusion_tag('firewall/tag/group_filter.sh')
def firewall_group_filter(group):
    return {
        'group': group,
        'rulekit': group.rulekit,
        'rule_list': group.rulekit.get_rules(),
    }


@register.inclusion_tag('firewall/tag/group_classifier.sh')
def firewall_group_classifier(chain_a, chain_b):
    return {
        'chain_a': chain_a,
        'chain_b': chain_b,
        'ip4_list': Ip4Entry.objects.all(),
    }
