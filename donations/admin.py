from django.contrib import admin
from donations.models import DonationTarget, Donation


def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)


def activate(modeladmin, request, queryset):
    queryset.update(active=True)


class DonationAdmin(admin.ModelAdmin):
    list_display = ("completed", "target", "amount")
    list_filter = ("target", "completed")
    date_hierarchy = "completed"


class DonationTargetAdmin(admin.ModelAdmin):
    list_display = ("label", "active")
    list_filter = ("active",)
    actions = [deactivate, activate]


admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationTarget, DonationTargetAdmin)
