from django.contrib import admin

from payments.models import SubscriptionInformation

class AlumniListDisplay:

    def alumni_fullName(self, x):
        return x.fullName
    alumni_fullName.short_description = 'Full Name'

    def approval_approval(self, x):
        return x.approval.approval
    approval_approval.short_description = 'Approved'
    approval_approval.boolean = 'true'
    approval_approval.admin_order_field = 'approval__approval'

    def setup_date(self, x):
        return x.setup.date
    setup_date.short_description = 'Setup Completed'
    setup_date.admin_order_field = 'setup__date'

    def profile_googleassociation(self, x):
        results = x.profile.googleassociation_set
        return results.exists()
    profile_googleassociation.short_description = 'Linked'
    profile_googleassociation.boolean = True
    profile_googleassociation.admin_order_field = 'profile__googleassociation'

    def approval_gsuite(self, x):
        return x.approval.gsuite
    approval_gsuite.short_description = 'Alumni E-Mail'
    approval_gsuite.admin_order_field = 'approval__gsuite'

    def payment_tier(self, x):
        return x.payment.tier
    payment_tier.short_description = 'Tier'
    payment_tier.admin_order_field = 'payment__tier'

    def atlas_included(self, x):
        return x.atlas.included
    atlas_included.short_description = 'Atlas'
    atlas_included.boolean = True
    atlas_included.admin_order_field = 'atlas__included'

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

    list_display = (
        # basic information
        'alumni_fullName', 'email', 'sex',

        # member email
        'approval_approval', 'setup_date', 'profile_googleassociation', 'approval_gsuite',

        # category + subscription
        'category', 'payment_tier',

        # visible in atalas
        'atlas_included',

        # Jacobs Information
        'jacobs_degree', 'jacobs_graduation', 'jacobs_major', 'jacobs_college',
    )


class SetupCompletedFilter(admin.SimpleListFilter):
    title = 'Setup Status'
    parameter_name = 'completed'

    def lookups(self, request, modeladmin):
        return [
            ('1', 'Completed'),
            ('0', 'Incomplete')
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val == '1':
            return queryset.filter(setup__isnull=False)
        elif val == '0':
            return queryset.filter(setup__isnull=True)
        else:
            return queryset

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class AlumniListFilter:
    # filters to the left
    list_filter = (
        ('approval__approval', custom_titled_filter('Application Approval')),
        SetupCompletedFilter,
        ('category', custom_titled_filter('Alumni Category')),
        ('payment__tier', custom_titled_filter('Alumni Tier')),
        ('atlas__included', custom_titled_filter('Included in Alumni Atlas')),
        ('jacobs__degree', custom_titled_filter('Jacobs Degree')),
        ('jacobs__graduation', custom_titled_filter('Jacobs Class')),
        ('jacobs__major', custom_titled_filter('Jacobs Major')),
    )
