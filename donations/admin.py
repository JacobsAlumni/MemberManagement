from django.contrib import admin
from donations.models import DonationTarget, Donation
from alumni.admin.actions import export_as_xslx_action

def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)


def activate(modeladmin, request, queryset):
    queryset.update(active=True)


class DonationAdmin(admin.ModelAdmin):
    list_display = ("completed", "target", "amount")
    list_filter = ("target", "completed")
    date_hierarchy = "completed"

    actions = [
        export_as_xslx_action("Export as XSLX", fields=["completed", "target"], extra_fields=[("amount", lambda x:x.amount)]),
    ]


class DonationTargetAdmin(admin.ModelAdmin):
    list_display = ("label", "active")
    list_filter = ("active",)
    actions = [deactivate, activate]


admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationTarget, DonationTargetAdmin)
