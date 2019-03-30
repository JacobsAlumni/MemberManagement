import stripe

from django.core.exceptions import ObjectDoesNotExist

from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin

from django.utils.decorators import method_decorator

from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from alumni.models import Approval
from registry.decorators import require_alumni
from registry.views.registry import default_alternative
from ..forms import RegistrationForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, SkillsForm, AtlasSettingsForm, SetupCompletedForm

from MemberManagement.mixins import RedirectResponseMixin

@method_decorator(login_required, name='dispatch')
class SetupView(RedirectResponseMixin, View):
    def get(self, *args, **kwargs):
        component = self.request.user.alumni.get_first_unset_component()

        if component is None:
            return self.redirect_response('portal', reverse=True)
        else:
            return self.redirect_response('setup_{}'.format(component), reverse=True)

class SetupViewBase(RedirectResponseMixin, TemplateResponseMixin, View):
    """ A base class for all setup views """


    http_method_names = ['get', 'post']
    template_name = 'setup/setup.html'
    
    setup_name = None
    setup_subtitle = ''
    setup_next_text = ''
    setup_form_class = None
    setup_redirect_url = 'setup'

    def has_setup_component(self):
        """ returns True iff this setup routine has already been performed """

        raise NotImplementedError

    def dispatch_already_set(self):
        """ called when setup component already exists """

        raise NotImplementedError
    
    def form_valid(self, form):
        """ Called when the form is valid and an instance is to be created """

        raise NotImplementedError

    def dispatch_success(self, validated):
        """ called upon successful setup """

        return self.redirect_response(self.__class__.setup_redirect_url, reverse=True)

    def get_context(self, form):
        """ builds context for instantiating the template """

        return {
            'form': form,
            'title': self.__class__.setup_name,
            'subtitle': self.__class__.setup_subtitle,
            'next_text': self.__class__.setup_next_text,
        }
    
    def dispatch(self, *args, **kwargs):
        # if we already have the setup component
        # then call the appropriate dispatch method
        if self.has_setup_component():
            return self.dispatch_already_set()

        # Create the form instance
        form = self.__class__.setup_form_class(self.request.POST or None)
        
        # and if it is valid
        if self.request.method == 'POST' and form.is_valid():
            form.clean()

            # and we successfully created the object
            return self.dispatch_success(self.form_valid(form))
        
        # else render the form
        return self.render_to_response(self.get_context(form))

class RegisterView(SetupViewBase):
    setup_name = 'Register'
    setup_subtitle = 'Enter your General Information - just the basics'
    setup_next_text = 'Continue Application'
    setup_form_class = RegistrationForm

    def has_setup_component(self):
        return self.request.user.is_authenticated

    def dispatch_already_set(self):
        return self.redirect_response('/')

    def form_valid(self, form):
        """ Called when the form is valid and an instance is to be created """

        # Create the user
        username = form.cleaned_data['username']
        user = User.objects.create_user(username, None, password=None)
        user.save()

        # Create the instance
        instance = form.save(commit=False)
        instance.profile = user
        instance.save()

        # Create an empty approval object
        approval = Approval(member=instance, approval=False, gsuite=None)
        approval.save()

        # authenticate the user    
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # and return the created user
        return instance

@method_decorator(require_alumni, name='dispatch')
class SetupComponentView(SetupViewBase):
    """ A view for setting up components """

    setup_next_text = 'Continue'

    @classmethod
    def setup_class(cls):
        return cls.setup_form_class.Meta.model

    def has_setup_component(self):
        return self.request.user.alumni.has_component(self.__class__.setup_class())

    def dispatch_already_set(self):
        return default_alternative(self.request)

    def form_valid(self, form):
        """ Called when the form is valid and an instance is to be created """
        instance = form.save(commit=False)
        instance.member = self.request.user.alumni
        instance.save()

        return instance


class AddressSetup(SetupComponentView):
    setup_name = 'General Information - Residential Address'
    setup_subtitle = ''
    setup_form_class = AddressForm

class SocialSetup(SetupComponentView):
    setup_name = 'Social Media Data'
    setup_subtitle = ''
    setup_form_class = SocialMediaForm

class JacobsSetup(SetupComponentView):
    setup_name = 'Alumni Data'
    setup_subtitle = 'tell us what you did at Jacobs'
    setup_form_class = JacobsForm

class JobSetup(SetupComponentView):
    setup_name = 'Professional Information'
    setup_subtitle = 'What did you do after Jacobs?'
    setup_form_class = JobInformationForm

class SkillsSetup(SetupComponentView):
    setup_name = 'Education And Skills'
    setup_subtitle = ''
    setup_form_class = SkillsForm

class AtlasSetup(SetupComponentView):
    setup_name = 'Atlas Setup'
    setup_subtitle = 'A Map & Search Interface for Alumni'
    setup_form_class = AtlasSettingsForm

class CompletedSetup(SetupComponentView):
    setup_name = 'Congratulations'
    setup_subtitle = '...'
    setup_form_class = SetupCompletedForm
    setup_next_text = 'Continue to Portal'

    template_name = 'setup/completed.html'
