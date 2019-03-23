from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(
        label='Your backup e-mail address',
        help_text='The private email you first used to register on the membership portal. ',
        max_length=100)