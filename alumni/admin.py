from django.contrib import admin
from .models import Alumni, Address, JobInformation, SocialMedia, \
    JacobsData, Approval, PaymentInformation


class AlumniJacobsDataInline(admin.StackedInline):
    model = JacobsData


class AlumniSocialMediaInline(admin.StackedInline):
    model = SocialMedia


class AlumniAddressInline(admin.StackedInline):
    model = Address


class AlumniJobsInline(admin.StackedInline):
    model = JobInformation


class AlumniApprovalInline(admin.StackedInline):
    model = Approval

class PaymentInline(admin.StackedInline):
    model = PaymentInformation


class AlumniAdmin(admin.ModelAdmin):
    inlines = [AlumniApprovalInline, AlumniAddressInline,
               AlumniJacobsDataInline, AlumniJobsInline,
               AlumniSocialMediaInline, PaymentInline]

    list_display = (
        # basic information
        'fullName', 'email', 'userApproval', 'sex', 'birthday', 'category',
        'paymentTier',

        # Jacobs information
        'jacobs_degree', 'jacobs_graduation', 'jacobs_major', 'jacobs_college',
    )

    list_filter = (
        'approval__approval', 'category', 'jacobs__degree',
        'jacobs__graduation',
        'jacobs__major', 'payment__tier')

    def fullName(self, x):
        return '{} {} {}'.format(x.firstName, x.middleName, x.lastName)

    fullName.short_description = 'Full Name'

    def userApproval(self, x):
        return x.approval.approval

    userApproval.short_description = 'Approval'
    userApproval.admin_order_field = 'approval__approval'

    def paymentTier(self, x):
        return x.payment.tier

    paymentTier.short_description = 'Tier'
    paymentTier.admin_order_field = 'payment__tier'

    def jacobs_degree(self, x):
        return x.jacobs.degree

    jacobs_degree.short_description = 'Degree'
    jacobs_degree.admin_order_field = 'jacobs__degree'

    def jacobs_graduation(self, x):
        return x.jacobs.graduation

    jacobs_graduation.short_description = 'Class'
    jacobs_graduation.admin_order_field = 'jacobs__graduation'

    def jacobs_major(self, x):
        return x.jacobs.major

    jacobs_major.short_description = 'Major'
    jacobs_major.admin_order_field = 'jacobs__major'

    def jacobs_college(self, x):
        return x.jacobs.college

    jacobs_college.short_description = 'College'
    jacobs_college.admin_order_field = 'jacobs__college'


admin.site.register(Alumni, AlumniAdmin)
