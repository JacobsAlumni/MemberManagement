from __future__ import annotations

from django import forms


class UserApprovalForm(forms.Form):
    email = forms.EmailField(label="E-Mail to assign to user")

    def clean_email(self) -> str:
        data = self.cleaned_data["email"]
        if not data.endswith("@jacobs-alumni.de"):
            raise forms.ValidationError("Email has to end in @jacobs-alumni.de")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
