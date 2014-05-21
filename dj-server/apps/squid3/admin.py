from django.contrib import admin

from .models import InterceptFilter, ExcludeUser


class InterceptFilterAdmin(admin.ModelAdmin):

    list_filter = (
        'enabled',
    )
    list_display = (
        'classifier',
        'squid_port',
        'enabled',
    )

admin.site.register(InterceptFilter, InterceptFilterAdmin)
admin.site.register(ExcludeUser)
