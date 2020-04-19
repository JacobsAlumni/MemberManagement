from __future__ import annotations

from django import forms
from django.contrib.auth.models import User

from alumni.models import (Address, Alumni, JacobsData, JobInformation,
                           SetupCompleted, Skills, SocialMedia)
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

    def clean_profile_fields(self, cleaned_data: Dict[str, Any]) -> None:
        if not 'email' in cleaned_data:
            return
        email = cleaned_data['email'].lower().strip()
        for domain in EMAIL_BLACKLIST:
            if email.endswith('@' + domain):
                self.add_error('email', forms.ValidationError(
                    "Your private email address may not end with '@{}'. ".format(domain)))
                return


class RegistrationForm(RegistrationMixin, forms.Form):
    """ A form for registering users """

    givenNames = forms.CharField(required=True)
    middleNames = forms.CharField(required=False)
    familyNames = forms.CharField(required=True)

    email = forms.EmailField(required=True)
    birthday = forms.DateField()

    memberType = forms.ChoiceField(choices=AlumniCategoryField.CHOICES)
    memberTier = forms.ChoiceField(choices=TierField.CHOICES)

    tos = forms.BooleanField(required=True)

    def clean(self) -> None:
        # individual field's clean methods have already been called
        cleaned_data = self.cleaned_data

        # check that the username doesn't already exist
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            self.add_error('username', forms.ValidationError(
                "This username is already taken, please pick another. "))
            return self.raise_validation_error()

        # check that we have accepted the terms and conditions
        if 'tos' not in self.cleaned_data or not self.cleaned_data['tos']:
            self.add_error('tos', forms.ValidationError(
                "You need to accept the terms and conditions to continue. "))
            return self.raise_validation_error()

        self.clean_profile_fields(cleaned_data)

        return super().clean()


class AlumniForm(RegistrationMixin, forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['givenName', 'middleName', 'familyName', 'email', 'sex',
                  'birthday', 'nationality', 'category']
        widgets = {
            'birthday': DatePickerInput()
        }
        help_texts = {
            "birthday": "",
        }

    def clean(self) -> None:
        self.clean_profile_fields(self.cleaned_data)
        return super().clean()


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
