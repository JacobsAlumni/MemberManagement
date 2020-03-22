from __future__ import annotations

from payments import stripewrapper

from django import forms

from payments.models import MembershipInformation

from alumni.fields import PaymentTypeField

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any


class MembershipInformationForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields['tier'].help_text = None

    class Meta:
        model = MembershipInformation
        fields = ['tier']


class PaymentMethodForm(forms.Form):
    payment_type = forms.ChoiceField(choices=PaymentTypeField.CHOICES)
    source_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    card_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self) -> Any:
        cleaned_data = self.cleaned_data

        # extract source id
        if 'source_id' in cleaned_data:
            source_id = cleaned_data['source_id']
        else:
            source_id = None
        cleaned_data['source_id'] = source_id
        source_is_blank = source_id == '' or source_id is None

        # extract card id
        if 'card_token' in cleaned_data:
            card_token = cleaned_data['card_token']
        else:
            card_token = None
        cleaned_data['card_token'] = card_token
        card_is_blank = card_token == '' or card_token is None

        if source_is_blank and card_is_blank:
            raise forms.ValidationError(
                'Either a Source ID or a Card Token must be given')

        if (not source_is_blank) and (not card_is_blank):
            raise forms.ValidationError(
                'Exactly one of Source ID and Card Token must be given')

        return cleaned_data

    def attach_to_customer(self, customer: str) -> [Optional[bool], Optional[str]]:
        source_id = self.cleaned_data['source_id']
        token = self.cleaned_data['card_token']
        return stripewrapper.update_payment_method(customer, source_id, token)


class CancellablePaymentMethodForm(PaymentMethodForm):
    go_to_starter = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self) -> Any:
        cleaned_data = self.cleaned_data

        # if 'go to starter' is set, go to starter instead
        if 'go_to_starter' in cleaned_data:
            if cleaned_data['go_to_starter'] == 'true':
                return cleaned_data
            else:
                cleaned_data['go_to_starter'] = ''

        return super().clean()

    @property
    def user_go_to_starter(self) -> bool:
        return self.cleaned_data['go_to_starter'] == 'true'

    def attach_to_customer(self, customer: str) -> [Optional[bool], Optional[str]]:
        # if go to starter was set, don't do anything
        if self.cleaned_data['go_to_starter']:
            return True, None

        return super().attach_to_customer(customer)
