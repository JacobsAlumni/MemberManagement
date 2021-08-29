from __future__ import annotations

import datetime

from django import forms

from alumni.fields import CountryField

from alumni.models import (Address, Alumni, JacobsData, JobInformation,
                           SetupCompleted, Skills, SocialMedia)
from payments.models import MembershipInformation
from alumni.fields import AlumniCategoryField, TierField
from atlas.models import AtlasSettings
from django_forms_uikit.widgets import DatePickerInput

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, Any

EMAIL_BLACKLIST = [
    'jacobs-alumni.de',
    'jacobs-alumni.com',
    'jacobs-alumni.eu',
    'jacobs-university.de'
]


class RegistrationMixin():
    def raise_validation_error(self) -> None:
        raise forms.ValidationError("Please correct the error below.")

    def clean(self) -> None:
        cleaned_data = self.cleaned_data

        # check that email is valid
        if 'email' in cleaned_data:
            self._validate_email(cleaned_data['email'])

        # check that the birthday is valid
        if 'birthday' in cleaned_data:
            self._validate_birthday(cleaned_data['birthday'])

        # check that tos are accepted
        if 'tos' in cleaned_data:
            self._validate_tos(cleaned_data['tos'])

        # check that we have an allowed tier and type
        if 'memberTier' in cleaned_data and 'memberCategory' in cleaned_data:
            self._validate_category(
                cleaned_data['memberTier'], cleaned_data['memberCategory'])

    def _validate_email(self, email: str) -> None:
        # validate that the email isn't blacklisted
        email = email.lower().strip()
        for domain in EMAIL_BLACKLIST:
            if email.endswith('@' + domain):
                self.add_error('email', forms.ValidationError(
                    "Your private email address may not end with '@{}'. ".format(domain)))
                return

    def _validate_birthday(self, birthday: datetime.date) -> None:
        # compute 18 years ago
        today = datetime.date.today()
        try:
            eighteen_years_ago = today.replace(year=today.year - 18)
        except ValueError:
            eighteen_years_ago = today.replace(
                year=today.year - 18, day=today.day - 1)

        # user must have been born 18 years
        if birthday > eighteen_years_ago:
            self.add_error('birthday', forms.ValidationError(
                "You must be at least 18 years old to become an Alumni member"))

    def _validate_tos(self, tos: bool) -> None:
        if not tos:
            self.add_error('tos', forms.ValidationError(
                "You mus accept the terms and conditions to continue"))

    def _validate_category(self, tier: str, category: str):
        if not MembershipInformation.allow_tier_and_category(tier, category):
            self.add_error('memberCategory', forms.ValidationError(
                "You have selected an invalid membership / tier combination"))


class RegistrationForm(RegistrationMixin, forms.Form):
    """ A form for registering users """

    givenName = forms.CharField(required=True)
    middleName = forms.CharField(required=False)
    familyName = forms.CharField(required=True)

    email = forms.EmailField(required=True)
    birthday = forms.DateField()

    memberCategory = forms.ChoiceField(choices=AlumniCategoryField.CHOICES)
    memberTier = forms.ChoiceField(choices=TierField.CHOICES)

    nationality = CountryField(multiple=True).formfield()

    tos = forms.BooleanField(required=True)


class AlumniForm(RegistrationMixin, forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['givenName', 'middleName', 'familyName', 'email', 'sex',
                  'birthday', 'nationality']
        widgets = {
            'birthday': DatePickerInput()
        }
        help_texts = {
            "birthday": "",
        }


class AddressForm(forms.ModelForm):
    """ A form for the Address of an Alumni """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_line_1'].required = True
        self.fields['city'].required = True
        self.fields['zip'].required = True
        self.fields['country'].required = True

    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'zip', 'city', 'state',
                  'country']


class JacobsForm(forms.ModelForm):
    """ A form for saving the users Jacobs Data """

    class Meta:
        model = JacobsData
        fields = ['college', 'degree', 'graduation', 'major', 'comments']
        labels = {
            'college': 'College',
            'degree': 'Degree',
            'graduation': 'Class (first graduation)',
            'major': 'Major',
            'comments': 'Comments'
        }


# TODO: Check that social media links are actually valid links for the platform
class SocialMediaForm(forms.ModelForm):
    """ A form for saving the users Social Media Data """

    class Meta:
        model = SocialMedia
        fields = ['facebook', 'linkedin', 'twitter', 'instagram', 'homepage']


class SkillsForm(forms.ModelForm):
    """ A form for saving the users Skills Data """

    class Meta:
        model = Skills
        fields = [
            'otherDegrees', 'spokenLanguages', 'programmingLanguages',
            'areasOfInterest', 'alumniMentor'
        ]
        labels = {
            'otherDegrees': 'Degrees from other instiutions:',
            'spokenLanguages': 'Spoken Languages:',
            'programmingLanguages': 'Programming Languages',
            'areasOfInterest': 'Areas of interest/expertise',
            'alumniMentor': ''
        }


class JobInformationForm(forms.ModelForm):
    """ A form for saving the users Job Information Data """

    class Meta:
        model = JobInformation
        fields = ['employer', 'position', 'industry', 'job']


class AtlasSettingsForm(forms.ModelForm):
    """ A form for saving the users Atlas Settings """

    class Meta:
        model = AtlasSettings
        fields = ['included', 'birthdayVisible', 'contactInfoVisible']
        labels = {
            'included': '',
            'birthdayVisible': '',
            'contactInfoVisible': '',
        }


class SetupCompletedForm(forms.ModelForm):
    class Meta:
        model = SetupCompleted
        fields = []
