from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.DonationReceipt)
class DonationReceiptAdmin(admin.ModelAdmin):
    pass
