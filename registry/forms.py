from django import forms
from alumni.models import Alumni, Address, JacobsData, SocialMedia, \
    JobInformation, PaymentInformation
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """ A form for registering users """
    username = forms.SlugField(label='Username',
                               help_text='A username for the admin portal. ')
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                label='Password',
                                help_text="Pick a password of at least 8 characters")
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                label='Password (again)',
                                help_text="Re-enter your password")

    tos = forms.BooleanField(label='Terms and Conditions',
                             help_text="I confirm that I have read and accepted the Terms and Conditions. ")

    class Meta:
        model = Alumni
        fields = ['firstName', 'middleName', 'lastName', 'email', 'sex',
                  'birthday', 'nationality', 'category']

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called

        # check that the passwords are identical
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', forms.ValidationError(
                "Please make sure that the password you entered is correct. "))
            raise forms.ValidationError("Please correct the error below.")

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
        fields = ['college', 'degree', 'graduation', 'major']


# TODO: Check that social media links are actually valid links for the platform
class SocialMediaForm(forms.ModelForm):
    """ A form for saving the users Social Media Data """

    class Meta:
        model = SocialMedia
        fields = ['facebook', 'twitter', 'linkedin', 'instagram', 'homepage']


class JobInformationForm(forms.ModelForm):
    """ A form for saving the users Job Information Data """

    class Meta:
        model = JobInformation
        fields = ['employer', 'position', 'industry', 'job']


class PaymentInformationForm(forms.ModelForm):
    """ A form for editing payment information"""

    class Meta:
        model = PaymentInformation
        fields = ['tier', 'token']
