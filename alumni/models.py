import bisect
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from custom_auth.mailutils import send_email

from . import fields

class Alumni(models.Model):
    """ The information about an Alumni Member """

    profile = models.OneToOneField(User, on_delete=models.CASCADE)

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

    # TODO: Better handling of multiple nationalities
    nationality = fields.CountryField(
        help_text="You can select multiple options by holding the <em>Ctrl</em> key (or <em>Command</em> on Mac) while clicking",
        multiple=True)

    # kind
    category = fields.AlumniCategoryField()

    #
    # COMPONENTS MANAGEMENT
    #

    # The list of components an prios of them
    components = []
    component_prios = []

    @classmethod
    def register_component(cls, prio):
        """ A decorator to add a component to the list of components """
        def decorator(f):
            # Find the insertion point within the priority list
            insertion = bisect.bisect_left(cls.component_prios, prio)

            # Insert into (components, component_prios)
            cls.components.insert(insertion, f)
            cls.component_prios.insert(insertion, prio)

            # and return the original function
            return f
        return decorator

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

        for c in self.__class__.components:
            name = c.member.field.remote_field.name
            if not self.has_component(name):
                return name

        return None
    
    @property
    def setup_completed(self):
        """ Checks if a user has completed setup """
        return self.get_first_unset_component() is None

    def __str__(self):
        return "Alumni [{}]".format(self.fullName)

    def send_welcome_email(self, password=None, back=False):
        """ Sends a user a Welcome (or welcome back) email """

        # Extract all the fields from the alumni
        email = self.email
        gsuite = self.approval.gsuite
        name = self.fullName
        tier = {
            fields.TierField.PATRON: 'Patron',
            fields.TierField.CONTRIBUTOR: 'Contributor',
            fields.TierField.STARTER: 'Starter'
        }[self.payment.tier]

        # set destination and instantiate email templates
        destination = [email, gsuite] + settings.GSUITE_EMAIL_ALL
        if back or password is None:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOMEBACK_SUBJECT, 'emails/welcomeback_email.html', name = name, tier = tier, gsuite = gsuite, password = password)
        else:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOME_SUBJECT, 'emails/welcome_email.html', name = name, tier = tier, gsuite = gsuite, password = password)



@Alumni.register_component(0)
class Address(models.Model):
    """ The address of an Alumni Member """

    member = models.OneToOneField(Alumni, related_name='address', on_delete=models.CASCADE)

    address_line_1 = models.CharField(max_length=255,
                                      help_text="E.g. Campus Ring 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="E.g. Apt 007 (optional)")
    city = models.CharField(max_length=255, help_text="E.g. Bremen")
    zip = models.CharField(max_length=255, help_text="E.g. 28759")
    state = models.CharField(max_length=255, blank=True, null=True,
                             help_text="E.g. Bremen (optional)")
    country = fields.CountryField()
    
    @property
    def coords(self, default=None):
        """ The coordinates of this user """
        from atlas.models import GeoLocation
        lat, lng = GeoLocation.getLoc(self.country, self.zip)
        if lat is None or lng is None:
            return [None, None]
        else:
            return [lat, lng]
       
    @classmethod
    def all_valid_coords(cls):
        """ Returns the coordinates of all alumni """
        coords = map(lambda x: x.coords, cls.objects.filter(member__atlas__included=True, member__approval__approval=True))
        return filter(lambda c: c[0] is not None and c[1] is not None, coords)


@Alumni.register_component(1)
class SocialMedia(models.Model):
    """ The social media data of a Jacobs Alumni """

    member = models.OneToOneField(Alumni, related_name='social', on_delete=models.CASCADE)

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


@Alumni.register_component(2)
class JacobsData(models.Model):
    """ The jacobs data of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='jacobs', on_delete=models.CASCADE)

    college = fields.CollegeField(null=True, blank=True)
    graduation = fields.ClassField()
    degree = fields.DegreeField(null=True, blank=True)
    major = fields.MajorField()
    comments = models.TextField(null=True, blank=True,
                                help_text="e.g. exchange semester, several degrees etc.")


class Approval(models.Model):
    """ The approval status of a member """
    member = models.OneToOneField(Alumni, related_name='approval', on_delete=models.CASCADE)

    approval = models.BooleanField(default=False, blank=True,
                                   help_text="Has the user been approved by an admin?")

    gsuite = models.EmailField(blank=True, null=True,
                               help_text="The G-Suite E-Mail of the user", unique=True)


@Alumni.register_component(3)
class JobInformation(models.Model):
    """ The jobs of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='job', on_delete=models.CASCADE)

    employer = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your employer (optional)")
    position = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your position (optional)")
    industry = fields.IndustryField()
    job = fields.JobField()


@Alumni.register_component(4)
class Skills(models.Model):
    """ The skills of an Alumni member """

    member = models.OneToOneField(Alumni, related_name='skills', on_delete=models.CASCADE)

    otherDegrees = models.TextField(null=True, blank=True)
    spokenLanguages = models.TextField(null=True, blank=True)
    programmingLanguages = models.TextField(null=True, blank=True)
    areasOfInterest = models.TextField(null=True, blank=True,
                                       help_text="E.g. Start-Ups, Surfing, Big Data, Human Rights, etc")
    alumniMentor = models.BooleanField(default=False, blank=True,
                                       help_text="I would like to sign up as an alumni mentor")

