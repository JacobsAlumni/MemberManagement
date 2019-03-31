from django.contrib import admin

from .models import PaymentInformation

class PaymentInformationInline(admin.StackedInline):
    model = PaymentInformation