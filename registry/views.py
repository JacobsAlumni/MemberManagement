from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistrationForm


def home(request):
    """ Renders either the home page or the portal. """

    if request.user.is_authenticated():
        return render(request, 'registry/portal/index.html',
                      {'user': request.user})
    else:
        return render(request, 'registry/index.html')


def register(request):
    """ Implements the new Alumni Registration Page"""

    # not for already logged in users
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        # load the form
        form = RegistrationForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # create a user object and save it
            username, password = \
                form.cleaned_data['username'], form.cleaned_data['password1']
            user = User.objects.create_user(username, None, password=password)
            user.save()

            # Create the Alumni Data Object
            instance = form.save(commit=False)
            instance.profile = user
            instance.save()

            # Authenticate the user for this request
            login(request, user)

            # and then redirect the user to the main profile page
            return redirect('/')

    # if we did not have any post data, simply create a new form
    else:
        form = RegistrationForm()

    # and return the request
    return render(request, 'registration/register.html', {'form': form})