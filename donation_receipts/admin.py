from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.DonationReceipt)
class DonationReceiptAdmin(admin.ModelAdmin):
    readonly_fields = ('receipt_pdf', )
    list_display = ('get_user_name', 'received_on', 'amount')
    list_filter = ('finalized', )
    date_hierarchy = 'received_on'

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj and not obj.finalized)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj and not obj.finalized)

    def get_user_name(self, obj):
        try:
            return str(obj.received_from.alumni.fullName)
        except:
            return obj.received_from.get_full_name()

    get_user_name.short_description = 'Received From'