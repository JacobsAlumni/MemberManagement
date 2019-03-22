from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Your backup e-mail address',
        max_length=100)