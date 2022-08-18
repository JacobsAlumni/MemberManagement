from django import forms
from djmoney.forms import fields as money_fields

class DonateForm(forms.Form):
    amount = money_fields.MoneyField(currency_choices=["EUR"])
    email = forms.EmailField()
    donation_for = forms.Select(choices=)