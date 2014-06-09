from django.contrib import admin

from .models import (
    ExcludedFilter,
    ExcludedUser,
    InterceptFilter,
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


admin.site.register(ExcludedFilter, ExcludedFilterAdmin)
admin.site.register(ExcludedUser)
admin.site.register(InterceptFilter, InterceptFilterAdmin)
