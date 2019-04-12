from django.contrib import admin

from ..models import Alumni, Address, JobInformation, SocialMedia, \
    JacobsData, Approval, Skills, SetupCompleted

from atlas.admin import AtlasSettingsInline
from payments.admin import MembershipInformationInline, SubscriptionInformationInline


class JacobsDataInline(admin.StackedInline):
    model = JacobsData


class SocialMediaInline(admin.StackedInline):
    model = SocialMedia


class AddressInline(admin.StackedInline):
    model = Address


class JobInformationInline(admin.StackedInline):
    model = JobInformation


class ApprovalInline(admin.StackedInline):
    model = Approval


class SkillsInline(admin.StackedInline):
    model = Skills


class SetupCompletedInline(admin.StackedInline):
    model = SetupCompleted


class AlumniAdminInlines:
    inlines = [SetupCompletedInline, ApprovalInline, AddressInline, SocialMediaInline, JacobsDataInline,
               JobInformationInline, SkillsInline, MembershipInformationInline, SubscriptionInformationInline, AtlasSettingsInline]
