from django.contrib import admin

from .models import (
    ExcludedFilter,
    ExcludedUser,
    InterceptFilter,
    L2Domain,
    Domain,
    SquidLog,
    DomainClassifierKit,
    DomainClassifier,
    DomainFilterKit,
    DomainFilter,
)


class ExcludedFilterAdmin(admin.ModelAdmin):

    list_filter = (
        'enabled',
    )
    list_display = (
        'classifier_kit',
        'enabled',
    )


class InterceptFilterAdmin(admin.ModelAdmin):

    list_filter = (
        'enabled',
    )
    list_display = (
        'classifier_kit',
        'squid_port',
        'enabled',
    )


class SquidLogAdmin(admin.ModelAdmin):

    list_display = (
        'access_date',
        'user',
        'domain',
        'size',
    )


class DomainClassifierAdmin(admin.ModelAdmin):

    list_filter = (
        'classifier_kit',
    )
    list_display = (
        'classifier_kit',
        'l2_domain',
        'domain',
        'reg_expr',
    )

class DomainClassifierInline(admin.StackedInline):
    model = DomainClassifier
    extra = 5


class DomainClassifierKitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    inlines = [DomainClassifierInline, ]

class DomainFilterAdmin(admin.ModelAdmin):

    list_filter = (
        'classifier_kit',
        'domain_filter_kit',
    )
    list_display = (
        'domain_filter_kit',
        'classifier_kit',
        'allow',
        'weight',
    )


class DomainFilterInline(admin.StackedInline):
    model = DomainFilter
    extra = 5


class DomainFilterKitAdmin(admin.ModelAdmin):

    list_display = (
        'group',
        'default_allow',
    )
    inlines = [DomainFilterInline, ]


admin.site.register(ExcludedFilter, ExcludedFilterAdmin)
admin.site.register(ExcludedUser)
admin.site.register(InterceptFilter, InterceptFilterAdmin)
admin.site.register(L2Domain)
admin.site.register(Domain)
admin.site.register(SquidLog, SquidLogAdmin)
admin.site.register(DomainClassifierKit, DomainClassifierKitAdmin)
#admin.site.register(DomainClassifier, DomainClassifierAdmin)
admin.site.register(DomainFilterKit, DomainFilterKitAdmin)
#admin.site.register(DomainFilter, DomainFilterAdmin)
