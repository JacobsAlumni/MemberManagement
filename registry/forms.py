from django import forms

from alumni.models import Alumni, Address, JacobsData, SocialMedia, \
    JobInformation, Skills, SetupCompleted
from atlas.models import AtlasSettings
from django.contrib.auth.models import User
from django_forms_uikit.widgets import DatePickerInput


class RegistrationMixin():
    def raise_validation_error(self):
        raise forms.ValidationError("Please correct the error below.")

    def clean_profile_fields(self, cleaned_data):
        if not 'email' in cleaned_data:
            return
        if cleaned_data['email'].endswith('@jacobs-alumni.de'):
            self.add_error('email', forms.ValidationError(
                "Your private email address may not be a Jacobs Alumni email address. "))
            return
        if cleaned_data['email'].endswith('@jacobs-university.de'):
            self.add_error('email', forms.ValidationError(
                "Your private email address may not be a Jacobs University email address. "))
            return


class RegistrationForm(RegistrationMixin, forms.ModelForm):
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
        # individual field's clean methods have already been called
        cleaned_data = self.cleaned_data

        # check that the username doesn't already exist
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            self.add_error('username', forms.ValidationError(
                "This username is already taken, please pick another. "))
            return self.raise_validation_error()

        # check that we have accepted the terms and conditions
        if not self.cleaned_data['tos']:
            self.add_error('tos', forms.ValidationError(
                "You need to accept the terms and conditions to continue. "))
            return self.raise_validation_error()

        self.clean_profile_fields(cleaned_data)

        return super().clean()


class AlumniForm(RegistrationMixin, forms.ModelForm):
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

    def clean(self):
        self.clean_profile_fields(self.cleaned_data)
        return super().clean()


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


class SetupCompletedForm(forms.ModelForm):
    class Meta:
        model = SetupCompleted
        fields = []
