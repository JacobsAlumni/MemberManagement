from django.contrib import admin

from .models import MembershipInformation, SubscriptionInformation


class MembershipInformationInline(admin.StackedInline):
    model = MembershipInformation
    extra = 0


class SubscriptionInformationInline(admin.TabularInline):
    model = SubscriptionInformation
    extra = 0
