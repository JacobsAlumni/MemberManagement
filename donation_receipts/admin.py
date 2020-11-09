from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.DonationReceipt)
class DonationReceiptAdmin(admin.ModelAdmin):
    readonly_fields = ('receipt_pdf', )
    list_display = ('received_from', 'received_on', 'amount')
    list_filter = ('finalized', )
    date_hierarchy = 'received_on'

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj and not obj.finalized)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj and not obj.finalized)