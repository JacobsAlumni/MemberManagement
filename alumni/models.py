from django.db import models
from django.contrib.auth.models import User

from . import fields

from registry.alumni import AlumniRegistryMixin, AlumniComponentMixin
from custom_auth.alumni import AlumniEmailMixin
from payments.alumni import AlumniSubscriptionMixin

class Alumni(AlumniSubscriptionMixin, AlumniEmailMixin, AlumniRegistryMixin, models.Model):
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

    def __str__(self):
        return "Alumni [{}]".format(self.fullName)


@Alumni.register_component(0)
class Address(AlumniComponentMixin, models.Model):
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
class SocialMedia(AlumniComponentMixin, models.Model):
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
class JacobsData(AlumniComponentMixin, models.Model):
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
class JobInformation(AlumniComponentMixin, models.Model):
    """ The jobs of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='job', on_delete=models.CASCADE)

    employer = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your employer (optional)")
    position = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your position (optional)")
    industry = fields.IndustryField()
    job = fields.JobField()


@Alumni.register_component(4)
class Skills(AlumniComponentMixin, models.Model):
    """ The skills of an Alumni member """

    member = models.OneToOneField(Alumni, related_name='skills', on_delete=models.CASCADE)

    otherDegrees = models.TextField(null=True, blank=True)
    spokenLanguages = models.TextField(null=True, blank=True)
    programmingLanguages = models.TextField(null=True, blank=True)
    areasOfInterest = models.TextField(null=True, blank=True,
                                       help_text="E.g. Start-Ups, Surfing, Big Data, Human Rights, etc")
    alumniMentor = models.BooleanField(default=False, blank=True,
                                       help_text="I would like to sign up as an alumni mentor")

@Alumni.register_component(1000)
class SetupCompleted(AlumniComponentMixin, models.Model):
    member = models.OneToOneField(Alumni, related_name='setup', on_delete=models.CASCADE)
    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Setup Completed On {}'.format(self.date)