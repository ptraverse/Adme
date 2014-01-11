from django.contrib import admin
from adme_app.models import *

class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('target_url', 'payout_clicks_required', 'payout_description', 'expiry_date','expiry_amount','created_by_business')
        }),
    )

class LinkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('contract','short_form','bitly_long_url','bitly_hash','activated_by')
        }),
    )

admin.site.register(Contract, ContractAdmin)
admin.site.register(Link,LinkAdmin)
