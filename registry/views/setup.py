from __future__ import annotations

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateResponseMixin, View
from django.views.decorators.csrf import ensure_csrf_cookie

from alumni.models import Approval
from MemberManagement.mixins import RedirectResponseMixin
from registry.decorators import require_alumni

from ..forms import (AddressForm, AtlasSettingsForm, JacobsForm,
                     JobInformationForm, RegistrationForm, SetupCompletedForm,
                     SkillsForm, SocialMediaForm)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, Dict
    from django.http import HttpResponse
    from django.forms import Form
    from django.db.models import Model

@method_decorator(login_required, name='dispatch')
class SetupView(RedirectResponseMixin, View):
    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        component = self.request.user.alumni.get_first_unset_component()

        if component is None:
            return self.redirect_response('portal', reverse=True)
        else:
            uri, reverse = component.component_setup_url()
            return self.redirect_response(uri, reverse=reverse)


class SetupViewBase(RedirectResponseMixin, TemplateResponseMixin, View):
    """ A base class for all setup views """

    http_method_names = ['get', 'post']
    template_name: str = 'setup/setup.html'

    setup_name: Optional[str] = None
    setup_subtitle: str = ''
    setup_next_text: str = ''
    setup_form_class: Type[Form] = None
    setup_redirect_url: str = 'setup'

    def has_setup_component(self) -> bool:
        """ Function that is called on every request to check if this component has been setup """

        raise NotImplementedError

    def should_setup_component(self) -> bool:
        """ Function that is called to perform pre-setup hooks and check if further (user-based) setup is required """

        raise NotImplementedError

    def dispatch_already_set(self) -> HttpResponse:
        """ Called when the setup component is already setup """

        raise NotImplementedError

    def dispatch_should_not(self) -> HttpResponse:
        """ Called when the setup component is not setup and also should not be """

        return self.dispatch_already_set()

    def form_valid(self, form: Form) -> Any:
        """ Called when the setup form has been successfully submitted """
        raise NotImplementedError

    def dispatch_success(self, validated: Any) -> HttpResponse:
        """ Called on True-ish return of form_valid() with the returned value """

        return self.redirect_response(self.__class__.setup_redirect_url, reverse=True)

    def get_context(self, form: Form) -> Dict[str, Any]:
        """ Builds the context for instatiating the content when a page is rendered """

        return {
            'form': form,
            'title': self.__class__.setup_name,
            'subtitle': self.__class__.setup_subtitle,
            'next_text': self.__class__.setup_next_text,
        }

    def dispatch_form(self, form: Form) -> HttpResponse:
        """ Called to dispatch the form to be filled out """

        return self.render_to_response(self.get_context(form))

    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        """ Dispatches this form """

        # if we already have the setup component
        # then call the appropriate dispatch method
        if self.has_setup_component():
            return self.dispatch_already_set()

        # if we should not setup this component next
        # then call the apporpriate redirect
        if not self.should_setup_component():
            return self.dispatch_should_not()

        # Create the form instance
        form = self.__class__.setup_form_class(self.request.POST or None)

        # and if it is valid
        if self.request.method == 'POST' and form.is_valid():
            form.clean()

            # if we have a valid form with some success
            # then we dispatch it
            success = self.form_valid(form)
            if success is not None:
                return self.dispatch_success(success)

        # else render the form
        return self.dispatch_form(form)

class LegacyRegisterView(SetupViewBase):
    setup_name = 'Register'
    setup_subtitle = 'Enter your General Information - just the basics'
    setup_next_text = 'Continue Application'
    setup_form_class = RegistrationForm

    def has_setup_component(self) -> bool:
        return self.request.user.is_authenticated

    def should_setup_component(self) -> bool:
        return True

    def dispatch_already_set(self) -> HttpResponse:
        return self.redirect_response('root', reverse=True)

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
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
    def setup_class(cls) -> Type[Model]:
        return cls.setup_form_class.Meta.model

    def has_setup_component(self) -> bool:
        return self.request.user.alumni.has_component(self.__class__.setup_class())

    def should_setup_component(self) -> bool:
        component = self.request.user.alumni.get_first_unset_component()
        if component is None:
            return False

        return component is self.__class__.setup_class()

    def dispatch_already_set(self) -> HttpResponse:
        return self.redirect_response('portal', reverse=True)

    def form_valid(self, form: Form) -> Model:
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
    setup_name = 'Almost Done'
    setup_subtitle = ''
    setup_form_class = SetupCompletedForm
    setup_next_text = 'Finalize Application & Continue to Portal'

    template_name = 'setup/completed.html'
