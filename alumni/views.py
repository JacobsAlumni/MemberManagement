import random
import string

from django.views.generic import FormView, View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.conf import settings

from .forms import UserApprovalForm
from .models import Alumni

from custom_auth.models import GoogleAssociation
from custom_auth.gsuite import get_user_id, create_user, patch_user

from raven.contrib.django.raven_compat.models import client

EMAIL_OK = 0
EMAIL_DIFFERS = 1
EMAIL_DOESNOTEXIST = 2
EMAIL_LINKEDOTHER = 3

EMAIL_HUMAN = {
    EMAIL_OK: '',
    EMAIL_DIFFERS: 'Differs from assigned address',
    EMAIL_DOESNOTEXIST: 'Does not exist on GSuite',
    EMAIL_LINKEDOTHER: 'Linked to another account'
}


def check_existing_email(alumni, candidate=None):
    """ Checks consistency with the existing email field """

    # canidate to compare with
    if candidate is None:
        candidate = alumni.approval.gsuite

    # check if we are already linked
    emailLinked = alumni.profile.googleassociation_set.exists()

    if candidate and alumni.existingEmail and alumni.existingEmail != candidate:
        return EMAIL_DIFFERS

    # if we have not linked check if the email exists
    elif not emailLinked and alumni.existingEmail:
        google_user_id = get_user_id(alumni.existingEmail)
        if google_user_id is None:
            return EMAIL_DOESNOTEXIST
        elif GoogleAssociation.objects.filter(google_user_id=google_user_id).exists():
            return EMAIL_LINKEDOTHER

    return EMAIL_OK


def generate_random_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=settings.GSUITE_PASS_LENGTH))


@method_decorator(staff_member_required, name='dispatch')
class ApprovalView(FormView):
    template_name = 'approval/index.html'
    form_class = UserApprovalForm

    def get_context_data(self, **kwargs):
        context = super(ApprovalView, self).get_context_data(**kwargs)

        alumni = get_object_or_404(
            Alumni, profile__id=self.request.resolver_match.kwargs['id'])
        emailLinked = alumni.profile.googleassociation_set.exists()
        previousEmail = EMAIL_HUMAN[check_existing_email(alumni)]

        context.update(
            {'alumni': alumni, 'emailLinked': emailLinked, 'previousEmail': previousEmail})
        return context

    def form_valid(self, form):
        # grab the context
        context = self.get_context_data(form=form)

        # run the approval process, or fail with a message
        try:
            self.run_approval(self.request, context, form)
        except Exception as e:
            client.captureException()
            form.add_error(None, 'Account approval failed: {}'.format(e))

        # grab the context *again*, as things might have changed
        return self.render_to_response(self.get_context_data(form=form))

    def run_approval(self, request, context, form):
        """ Runs the approval process for a given user """
        alumni = context['alumni']

        # if the user is already approved, error out
        if alumni.approval.approval:
            raise Exception("Can not approve: Already approved. ")

        # if the email is already linked, error out
        if context['emailLinked']:
            raise Exception("User already has a linked account. ")

        # check that the existing email is ok
        email = form.cleaned_data['email']
        existingEmail = check_existing_email(alumni, candidate=email)
        if existingEmail != EMAIL_OK:

            raise Exception("Existing Email Field Problem: {}".format(
                EMAIL_HUMAN[existingEmail]))

        # decide what to do
        if not alumni.existingEmail:
            return self.run_approval_newaccount(request, email, alumni)
        elif alumni.resetExistingEmailPassword:
            return self.run_approval_reset_and_unlock(request, email, alumni)
        else:
            return self.run_approval_unlock(request, email, alumni)

    def run_approval_newaccount(self, request, email, alumni):
        """ Creates a new account for email """

        messages.info(
            request, 'Approving with a new account: {}'.format(email))

        # generate a random password to use for the user
        password = generate_random_password()

        # Create the new account
        messages.info(request, 'Creating a new account {}'.format(email))
        uid = create_user(alumni.firstName, alumni.lastName, email, password)
        if uid is None:
            raise ValueError(
                'Something went wrong while creating user account')
        messages.success(request, 'Created user with id {}'.format(uid))

        # Approve + Link
        self.approve_and_link(request, email, alumni)

        # Send email
        messages.info(request, 'Sending Welcome email')
        alumni.send_welcome_email(password=password)
        messages.success(request, 'Sent welcome email')

    def run_approval_unlock(self, request, email, alumni):
        """ Unlocks an existing account for alumni """

        messages.info(
            request, 'Approving with existing account: {}'.format(email))

        # Patch existing account
        messages.info(request, 'Patching account {}'.format(email))
        uid = patch_user(email)
        if uid is None:
            raise ValueError(
                'Something went wrong while patching user account')
        messages.success(request, 'Patched user with id {}'.format(uid))

        # Approve + Link
        self.approve_and_link(request, email, alumni)

        # Send email
        messages.info(request, 'Sending Welcome Back email')
        alumni.send_welcome_email(back=True)
        messages.success(request, 'Sent Welcome Back email')

    def run_approval_reset_and_unlock(self, request, email, alumni):
        """ Unlocks and resets an existing account """

        messages.info(
            request, 'Approving with reset for existing account: {}'.format(email))

        # generate a random password to reset the password to
        password = generate_random_password()

        # Patch existing account
        messages.info(request, 'Patching account + password {}'.format(email))
        uid = patch_user(email, password=password)
        if uid is None:
            raise ValueError(
                'Something went wrong while patching user account')
        messages.success(request, 'Patched user with id {}'.format(uid))

        # Approve + Link
        self.approve_and_link(request, email, alumni)

        # Send email
        messages.info(request, 'Sending Welcome Back email')
        alumni.send_welcome_email(password=password, back=True)
        messages.success(request, 'Sent Welcome Back email')

    def approve_and_link(self, request, email, alumni):
        # Approve user
        messages.info(request, 'Storing approval info')
        alumni.approval.approval = True
        alumni.approval.gsuite = email
        alumni.approval.time = timezone.now()
        alumni.approval.save()
        messages.success(request, 'Stored approval info')

        # Link user
        messages.info(request, 'Linking portal account')
        GoogleAssociation.link_user(alumni.profile)
        messages.success(request, 'Linked portal account')


@staff_member_required
def preview_welcome_email(request, uid):
    alumni = get_object_or_404(Alumni, profile__id=uid)
    return alumni.render_welcome_email(request, password='PasswordWillBeHere', back=False)


@staff_member_required
def preview_welcomeback_password_email(request, uid):
    alumni = get_object_or_404(Alumni, profile__id=uid)
    return alumni.render_welcome_email(request, password='PasswordWillBeHere', back=True)


@staff_member_required
def preview_welcomeback_link_email(request, uid):
    alumni = get_object_or_404(Alumni, profile__id=uid)
    return alumni.render_welcome_email(request, password=None, back=True)
