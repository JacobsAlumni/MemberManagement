from django.contrib import admin

from .models import MembershipInformation, SubscriptionInformation


class MembershipInformationInline(admin.StackedInline):
    model = MembershipInformation


class SubscriptionInformationInline(admin.TabularInline):
    model = SubscriptionInformation
    extra = 0
