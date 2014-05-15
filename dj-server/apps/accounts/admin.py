from django.contrib import admin

from .models import Profile, Ip4Entry


class ProfileAdmin(admin.ModelAdmin):

    list_filter = ('max_ip4_entry', )
    list_display = (
        'user',
        'full_name',
        'max_ip4_entry',
    )


class Ip4EntryAdmin(admin.ModelAdmin):

    list_filter = ('user', 'priority')
    list_display = (
        'user',
        'ip_address',
        'create_date',
        'update_date',
        'priority',
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ip4Entry, Ip4EntryAdmin)
