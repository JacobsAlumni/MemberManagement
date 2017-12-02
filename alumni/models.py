import collections
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django_countries.fields import CountryField
from . import fields


class Alumni(models.Model):
    """ The information about an Alumni Member """

    profile = models.OneToOneField(User)

    # name and basic contact information
    firstName = models.CharField(max_length=255, help_text="Your first name")
    middleName = models.CharField(max_length=255, blank=True, null=True,
                                  help_text="Your middle names (optional)")
    lastName = models.CharField(max_length=255, help_text="Your last name")

    @property
    def fullName(self):
        names = [self.firstName]

        if self.middleName is not None:
            names.append(self.middleName)

        names.append(self.lastName)

        return ' '.join(names)

    email = models.EmailField(help_text="Your private email address")

    # gender, nationality, birthday
    sex = fields.GenderField()
    birthday = models.DateField(
        help_text="Your birthday in the format YYYY-MM-DD")

    # TODO: Better handling of multiple nationalities
    nationality = CountryField(help_text="Your nationality", multiple=True)

    # kind
    category = fields.AlumniCategoryField()

    #
    # COMPONENTS MANAGEMENT
    #

    # The list of components know to this class
    components = collections.OrderedDict()

    @classmethod
    def register_component(cls, f):
        """ A decorator to add a component to the list of components """

        name = f.member.field.remote_field.name
        cls.components[name] = f
        return f

    def has_component(self, component):
        """ Checks if this alumni has a given component"""
        try:
            _ = getattr(self, component)
            return True
        except ObjectDoesNotExist:
            return False

    def get_first_unset_component(self):
        """ Gets the first unset component or returns None if it
        already exists. """

        for c in self.__class__.components.keys():
            if not self.has_component(c):
                return c

        return None

    def __str__(self):
        return "Alumni [{}]".format(self.fullName)


@Alumni.register_component
class Address(models.Model):
    """ The address of an Alumni Member """

    member = models.OneToOneField(Alumni, related_name='address')

    address_line_1 = models.CharField(max_length=255,
                                      help_text="E.g. Campus Ring 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="E.g. Apt 007 (optional)")
    city = models.CharField(max_length=255, help_text="E.g. Bremen")
    zip = models.CharField(max_length=255, help_text="E.g. 28759")
    state = models.CharField(max_length=255, blank=True, null=True,
                             help_text="E.g. Bremen (optional)")
    country = CountryField()


@Alumni.register_component
class JacobsData(models.Model):
    """ The jacobs data of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='jacobs')

    college = fields.CollegeField(null=True, blank=True)
    graduation = fields.ClassField()
    degree = fields.DegreeField(null=True, blank=True)
    major = fields.MajorField()



class Approval(models.Model):
    """ The approval status of a member """
    member = models.OneToOneField(Alumni, related_name='approval')

    approval = models.BooleanField(default=False,
                                   help_text="Has the user been approved by an admin?")


@Alumni.register_component
class SocialMedia(models.Model):
    """ The social media data of a Jacobs Alumni """

    member = models.OneToOneField(Alumni, related_name='social')

    facebook = models.URLField(null=True, blank=True,
                               help_text="Your Facebook Profile (optional)")
    twitter = models.URLField(null=True, blank=True,
                              help_text="Your Twitter Account (optional)")
    linkedin = models.URLField(null=True, blank=True,
                               help_text="Your LinkedIn Profile (optional)")
    instagram = models.URLField(null=True, blank=True,
                                help_text="Your Instagram (optional)")
    homepage = models.URLField(null=True, blank=True,
                               help_text="Your Homepage or Blog")


@Alumni.register_component
class JobInformation(models.Model):
    """ The jobs of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='job')

    employer = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your employer (optional)")
    position = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your position (optional)")
    industry = fields.IndustryField()
    job = fields.JobField()


@Alumni.register_component
class PaymentInformation(models.Model):
    """ The payment information of an Alumni Member """

    member = models.OneToOneField(Alumni, related_name='payment')

    tier = fields.TierField(help_text='Membership Tier')
    token = models.CharField(max_length=255, null=True, blank=True)
