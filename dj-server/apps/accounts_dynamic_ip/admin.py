from django.contrib import admin

from .models import DynamicAccounts


class DynamicAccountsAdmin(admin.ModelAdmin):

    list_filter = ('user', )


admin.site.register(DynamicAccounts, DynamicAccountsAdmin)
