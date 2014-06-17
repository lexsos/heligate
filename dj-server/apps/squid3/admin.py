from django.contrib import admin

from .models import (
    ExcludedFilter,
    ExcludedUser,
    InterceptFilter,
    L2Domain,
    Domain,
    SquidLog,
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


admin.site.register(ExcludedFilter, ExcludedFilterAdmin)
admin.site.register(ExcludedUser)
admin.site.register(InterceptFilter, InterceptFilterAdmin)
admin.site.register(L2Domain)
admin.site.register(Domain)
admin.site.register(SquidLog, SquidLogAdmin)
