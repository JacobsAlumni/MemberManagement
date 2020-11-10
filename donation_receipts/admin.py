from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models

# Register your models here.


@admin.register(models.DonationReceipt)
class DonationReceiptAdmin(admin.ModelAdmin):
    readonly_fields = ('receipt_pdf', 'issued_on')
    list_display = ('get_user_name', 'received_on', 'amount')
    list_filter = ('finalized', )
    date_hierarchy = 'received_on'

    fieldsets = (
        (None, {
            'fields': ('finalized', )
        }),
        (_('Donation Info'), {
            'fields': ('received_on', 'received_from', 'amount', 'sender_info')
        }),
        (_('Internal Tracking'), {
            'fields': ('payment_stream', 'payment_reference', 'internal_notes')
        })
    )

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj and not obj.finalized)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj and not obj.finalized)

    def get_user_name(self, obj):
        try:
            return str(obj.received_from.alumni.fullName)
        except:
            try:
                return obj.received_from.get_full_name()
            except:
                return None

    get_user_name.short_description = 'Received From'
