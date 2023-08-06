from __future__ import annotations

from django.contrib import admin

from .models import MembershipInformation, SubscriptionInformation, PaymentIntent


class ReadOnlyModelAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MembershipInformationInline(admin.StackedInline):
    model = MembershipInformation
    extra = 0


class SubscriptionInformationInline(admin.TabularInline):
    model = SubscriptionInformation
    extra = 0


@admin.register(PaymentIntent)
class PaymentIntentAdmin(ReadOnlyModelAdmin):
    pass
