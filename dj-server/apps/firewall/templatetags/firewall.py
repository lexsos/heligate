from __future__ import absolute_import

from django.template import Library


register = Library()


@register.inclusion_tag('firewall/tag/group_filter.sh')
def firewall_group_filter(group):
    return {
        'group': group,
        'rulekit': group.rulekit,
        'rule_list': group.rulekit.get_rules(),
    }
