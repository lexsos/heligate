from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):

    list_filter = (
        'applyed',
    )
    list_display = (
        'create_date',
        'event_id',
        'applyed',
    )

admin.site.register(Event, EventAdmin)
