from django.contrib import admin

from .models import StaticIp4


class StaticIp4Admin(admin.ModelAdmin):

    list_filter = ('user', )
    list_display = (
        'user',
        'ip_address',
    )


admin.site.register(StaticIp4, StaticIp4Admin)
