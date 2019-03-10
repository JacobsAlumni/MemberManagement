from django import forms

from alumni.models import Alumni, Address, JacobsData, SocialMedia, \
    JobInformation, PaymentInformation, Skills
from atlas.models import AtlasSettings
from django.contrib.auth.models import User
from django_forms_uikit.widgets import DatePickerInput


class RegistrationForm(forms.ModelForm):
    """ A form for registering users """
    username = forms.SlugField(label='Username',
                               help_text='Select your username for the membership portal. '
                                         'We recommend your alumni email username, e.g. <em>ppan</em> for <em>Peter Pan</em>')

    _tos_help_text = 'I confirm that I have read and agree to the ' \
                     '<a target="_blank" href="/privacy">Terms and Conditions' \
                     '</a>, the <a target="_blank" href="' \
                     'https://jacobs-alumni.de/charter">Charter</a>, and the ' \
                     '<a target="_blank" href="https://www.jacobs-alumni.de/by-laws">Contributions By-Laws</a>. '
    tos = forms.BooleanField(label='Terms and Conditions',
                             help_text=_tos_help_text)

    class Meta:
        model = Alumni
        fields = ['firstName', 'middleName', 'lastName', 'email',
                  'existingEmail', 'resetExistingEmailPassword', 'sex',
                  'birthday', 'nationality', 'category']
        widgets = {
            'birthday': DatePickerInput()
        }
        labels = {
            "firstName": "First Name",
            "middleName": "Middle Name",
            "lastName": "Last Name",
            "existingEmail": "",
            "resetExistingEmailPassword": ""
        }
        help_texts = {
            "birthday": "",
        }

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called

        # check that the username doesn't already exist
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            self.add_error('username', forms.ValidationError(
                "This username is already taken, please pick another. "))
            raise forms.ValidationError("Please correct the error below.")

        # check that we have accepted the terms and conditions
        if not self.cleaned_data['tos']:
            self.add_error('tos', forms.ValidationError(
                "You need to accept the terms and conditions to continue. "))
            raise forms.ValidationError("Please correct the error below.")

        return super(RegistrationForm, self).clean()


class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['firstName', 'middleName', 'lastName', 'email', 'sex',
                  'birthday', 'nationality', 'category']
        widgets = {
            'birthday': DatePickerInput()
        }
        help_texts = {
            "birthday": "",
        }


class AddressForm(forms.ModelForm):
    """ A form for the Address of an Alumni """

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


class PaymentInformationForm(forms.ModelForm):
    """ A form for editing payment information"""

    class Meta:
        model = PaymentInformation
        fields = ['tier', 'token', 'starterReason', 'payment_type', 'sepa_mandate']
        widgets = {'token': forms.HiddenInput(), 'sepa_mandate': forms.HiddenInput()}
        labels = {
            'starterReason': ''
        }

class UserApprovalForm(forms.Form):
    email = forms.EmailField(label='E-Mail to assign to user')

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data.endswith('@jacobs-alumni.de'):
            raise forms.ValidationError("Email has to end in @jacobs-alumni.de")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
