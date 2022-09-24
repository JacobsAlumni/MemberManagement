from django.contrib import admin

# Register your models here.
from donations.models import DonationTarget, Donation


class DonationAdmin(admin.ModelAdmin):
    list_display = ("completed", "target", "amount")
    list_filter = ("target",)
    date_hierarchy = "completed"


admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationTarget)
