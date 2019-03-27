from django import forms

from payments.models import PaymentInformation

class PaymentInformationForm(forms.ModelForm):
    """ A form for editing payment information"""

    class Meta:
        model = PaymentInformation
        fields = ['tier', 'token', 'starterReason', 'payment_type', 'sepa_mandate']
        widgets = {'token': forms.HiddenInput(), 'sepa_mandate': forms.HiddenInput()}
        labels = {
            'starterReason': ''
        }
