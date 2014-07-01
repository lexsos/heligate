from django.contrib import admin

from .models import RedirectUrl


class RedirectUrlAdmin(admin.ModelAdmin):

    list_display = (
        'create_date',
        'url',
    )


admin.site.register(RedirectUrl, RedirectUrlAdmin)
