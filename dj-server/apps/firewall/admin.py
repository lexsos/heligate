from django.contrib import admin

from .models import (
    IpFilter,
    NetInterface,
    Classifier,
    RuleSet,
    IpRule,
)


class IpFilterAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
    )


class NetInterfaceAdmin(admin.ModelAdmin):

    list_display = (
        'if_name',
        'description',
    )


class ClassifierAdmin(admin.ModelAdmin):

    list_filter = (
        'ip_filter',
        'ip_version',
        'protocol',
    )
    list_display = (
        'ip_filter',
        'ip_version',
        'protocol',
        'src_ip',
        'dst_ip',
        'src_ports',
        'dst_ports',
    )


class IpRuleInline(admin.StackedInline):
    model = IpRule
    extra = 10


class RuleSetAdmin(admin.ModelAdmin):

    list_display = (
        'group',
        'default_action',
    )

    inlines = [IpRuleInline, ]


class IpRuleAdmin(admin.ModelAdmin):

    list_filter = (
        'enabled',
        'weight',
        'rule_set',
    )
    list_display = (
        'rule_set',
        'ip_filter',
        'action',
        'enabled',
        'weight',
    )


admin.site.register(IpFilter, IpFilterAdmin)
admin.site.register(NetInterface, NetInterfaceAdmin)
admin.site.register(Classifier, ClassifierAdmin)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(IpRule, IpRuleAdmin)
