from django.contrib import admin

from .models import (
    ClassifierKit,
    NetInterface,
    Classifier,
    RuleKit,
    IpRule,
)


class ClassifierInline(admin.StackedInline):
    model = Classifier
    extra = 5


class ClassifierKitAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
    )
    inlines = [ClassifierInline, ]


class NetInterfaceAdmin(admin.ModelAdmin):

    list_display = (
        'if_name',
        'use_nat',
        'description',
    )


class ClassifierAdmin(admin.ModelAdmin):

    list_filter = (
        'classifier_kit',
        'ip_version',
        'protocol',
    )
    list_display = (
        'classifier_kit',
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


class RuleKitAdmin(admin.ModelAdmin):

    list_display = (
        'group',
        'default_action',
    )
    inlines = [IpRuleInline, ]


class IpRuleAdmin(admin.ModelAdmin):

    list_filter = (
        'enabled',
        'weight',
        'rule_kit',
    )
    list_display = (
        'rule_kit',
        'classifier_kit',
        'action',
        'enabled',
        'weight',
    )


admin.site.register(ClassifierKit, ClassifierKitAdmin)
admin.site.register(NetInterface, NetInterfaceAdmin)
admin.site.register(RuleKit, RuleKitAdmin)
