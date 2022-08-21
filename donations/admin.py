from django.contrib import admin

# Register your models here.
from donations.models import DonationTarget, Donation

admin.site.register(Donation)
admin.site.register(DonationTarget)
