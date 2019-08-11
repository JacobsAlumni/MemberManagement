from payments import stripewrapper

from django import forms

from payments.models import MembershipInformation
from raven.contrib.django.raven_compat.models import client

from alumni.fields import PaymentTypeField


class MembershipInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tier'].help_text = None

    class Meta:
        model = MembershipInformation
        fields = ['tier', 'starterReason']
        labels = {
            'starterReason': '',
        }


class PaymentMethodForm(forms.Form):
    payment_type = forms.ChoiceField(choices=PaymentTypeField.CHOICES)
    source_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    card_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = self.cleaned_data

        # extract source id
        if 'source_id' in cleaned_data:
            source_id = cleaned_data['source_id']
        else:
            source_id = None
        cleaned_data['source_id'] = source_id
        source_is_blank = source_id is '' or source_id is None

        # extract card id
        if 'card_token' in cleaned_data:
            card_token = cleaned_data['card_token']
        else:
            card_token = None
        cleaned_data['card_token'] = card_token
        card_is_blank = card_token is '' or card_token is None

        if source_is_blank and card_is_blank:
            raise forms.ValidationError(
                'Either a Source ID or a Card Token must be given')

        if (not source_is_blank) and (not card_is_blank):
            raise forms.ValidationError(
                'Exactly one of Source ID and Card Token must be given')

        return cleaned_data

    def attach_to_customer(self, customer):
        source_id = self.cleaned_data['source_id']
        token = self.cleaned_data['card_token']
        return stripewrapper.update_payment_method(customer, source_id, token)
