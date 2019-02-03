import collections
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from jsonfield import JSONField

from . import fields

import re

class Alumni(models.Model):
    """ The information about an Alumni Member """

    profile = models.OneToOneField(User)

    # name and basic contact information
    firstName = models.CharField(max_length=255, help_text="Your first name")
    middleName = models.CharField(max_length=255, blank=True, null=True,
                                  help_text="Your middle name(s)")
    lastName = models.CharField(max_length=255, help_text="Your last name")

    @property
    def fullName(self):
        names = [self.firstName]

        if self.middleName is not None:
            names.append(self.middleName)

        names.append(self.lastName)
        return ' '.join(names)

    email = models.EmailField(help_text="Your private email address", unique=True)
    existingEmail = models.EmailField(blank=True, null=True,
                                      help_text="Existing <em>@jacobs-alumni.de</em> email address (if you have one)")
    resetExistingEmailPassword = models.BooleanField(blank=True, default=False, help_text='Reset password to existing email address')

    # gender, nationality, birthday
    sex = fields.GenderField()
    birthday = models.DateField(
        help_text="Your birthday in YYYY-MM-DD format")
    birthdayVisible = models.BooleanField(default=False, blank=True,
                                          help_text="Make birthday visible to others")

    # TODO: Better handling of multiple nationalities
    nationality = fields.CountryField(
        help_text="You can select multiple options by holding the <em>Ctrl</em> key (or <em>Command</em> on Mac) while clicking",
        multiple=True)

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
    country = fields.CountryField()

    addressVisible = models.BooleanField(default=False, blank=True,
                                         help_text="Include me on the alumni map (only your city will be visible to others)")
    
    @property
    def coords(self, default=None):
        """ The coordinates of this user """
        lat, lng = GeoLocation.getLoc(self.country, self.zip)
        if lat is None or lng is None:
            return [None, None]
        else:
            return [lat, lng]
       
    @classmethod
    def all_valid_coords(cls):
        """ Returns the coordinates of all alumni """
        coords = map(lambda x: x.coords, cls.objects.filter(addressVisible=True, member__approval__approval=True))
        return filter(lambda c: c[0] is not None and c[1] is not None, coords)


@Alumni.register_component
class SocialMedia(models.Model):
    """ The social media data of a Jacobs Alumni """

    member = models.OneToOneField(Alumni, related_name='social')

    facebook = models.URLField(null=True, blank=True,
                               help_text="Your Facebook Profile (optional)")
    linkedin = models.URLField(null=True, blank=True,
                               help_text="Your LinkedIn Profile (optional)")
    twitter = models.URLField(null=True, blank=True,
                              help_text="Your Twitter Account (optional)")
    instagram = models.URLField(null=True, blank=True,
                                help_text="Your Instagram (optional)")
    homepage = models.URLField(null=True, blank=True,
                               help_text="Your Homepage or Blog")


@Alumni.register_component
class JacobsData(models.Model):
    """ The jacobs data of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='jacobs')

    college = fields.CollegeField(null=True, blank=True)
    graduation = fields.ClassField()
    degree = fields.DegreeField(null=True, blank=True)
    major = fields.MajorField()
    comments = models.TextField(null=True, blank=True,
                                help_text="e.g. exchange semester, several degrees etc.")


class Approval(models.Model):
    """ The approval status of a member """
    member = models.OneToOneField(Alumni, related_name='approval')

    approval = models.BooleanField(default=False, blank=True,
                                   help_text="Has the user been approved by an admin?")

    gsuite = models.EmailField(blank=True, null=True,
                               help_text="The G-Suite E-Mail of the user", unique=True)


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
class Skills(models.Model):
    """ The skills of an Alumni member """

    member = models.OneToOneField(Alumni, related_name='skills')

    otherDegrees = models.TextField(null=True, blank=True)
    spokenLanguages = models.TextField(null=True, blank=True)
    programmingLanguages = models.TextField(null=True, blank=True)
    areasOfInterest = models.TextField(null=True, blank=True,
                                       help_text="E.g. Start-Ups, Surfing, Big Data, Human Rights, etc")
    alumniMentor = models.BooleanField(default=False, blank=True,
                                       help_text="I would like to sign up as an alumni mentor")


@Alumni.register_component
class PaymentInformation(models.Model):
    """ The payment information of an Alumni Member """

    member = models.OneToOneField(Alumni, related_name='payment')

    tier = fields.TierField(help_text='Membership Tier')

    payment_type = fields.PaymentTypeField()

    starterReason = models.TextField(null=True, blank=True,
        help_text="")

    token = models.CharField(max_length=255, null=True, blank=True,
                             help_text='The stripe card token for the user')
    customer = models.CharField(max_length=255, null=True, blank=True,
                                help_text='The stripe customer id for the user')
    subscription = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='The payment token for the customer')
    sepa_mandate = JSONField(blank=True, null=True)

class GeoLocation(models.Model):
    """ Represents a (cached) GeoLocation """

    country = fields.CountryField()
    zip = models.CharField(max_length=10)

    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        unique_together = (('country', 'zip'))
        
    @classmethod
    def getLoc(cls, country, zip):
        try:
            instance = cls.objects.get(country=country, zip=cls.normalize_zip(zip))
        except cls.DoesNotExist:
            #print('No location for combination: ', country.code, cls.normalize_zip(zip))
            return None, None
        
        return instance.lat, instance.lon
    
    @classmethod
    def updateData(cls, data):
        with transaction.atomic():
            cls.objects.all().delete()
            cls.objects.bulk_create(data)
    
    @classmethod
    def normalize_zip(self, zip):
        lowerzip = zip.lower()
        return re.sub(r'[^0-9a-z]', '', lowerzip)
    
    def __str__(self):
        return 'GeoLocation of {} in {}'.format(self.zip, self.country)