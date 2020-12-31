from __future__ import annotations

from django.db import models
from django.contrib.auth.models import User

from . import fields

from registry.alumni import AlumniRegistryMixin, AlumniComponentMixin
from custom_auth.alumni import AlumniEmailMixin
from payments.alumni import AlumniSubscriptionMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional, Iterable, Union
    from datetime import date, datetime
    from django_countries.fields import Country
    from atlas.models import AtlasSettings
    from payments.models import MembershipInformation
    from atlas.models import GeoLocation


class Alumni(AlumniSubscriptionMixin, AlumniEmailMixin, AlumniRegistryMixin, models.Model):
    """ The information about an Alumni Member """

    profile: User = models.OneToOneField(User, on_delete=models.CASCADE)

    # name and basic contact information
    givenName: str = models.CharField(
        max_length=255, help_text="Your given name")
    middleName: Optional[str] = models.CharField(max_length=255, blank=True, null=True,
                                                 help_text="Your middle name(s)")
    familyName: str = models.CharField(
        max_length=255, help_text="Your family name")

    @property
    def fullName(self) -> str:
        names = [self.givenName]

        if self.middleName is not None:
            names.append(self.middleName)

        names.append(self.familyName)
        return ' '.join(names)

    email: str = models.EmailField(
        help_text="Your private email address", unique=True)
    existingEmail: Optional[str] = models.EmailField(blank=True, null=True,
                                                     help_text="Existing <em>@jacobs-alumni.de</em> email address (if you have one)")
    resetExistingEmailPassword: bool = models.BooleanField(
        blank=True, default=False, help_text='Reset password to existing email address')

    # gender, nationality, birthday
    sex: str = fields.GenderField()
    birthday: date = models.DateField(
        help_text="Your birthday in YYYY-MM-DD format")

    # TODO: Better handling of multiple nationalities
    nationality: Country = fields.CountryField(
        help_text="You can select multiple options by holding the <em>Ctrl</em> key (or <em>Command</em> on Mac) while clicking",
        multiple=True)

    # kind
    category: str = fields.AlumniCategoryField()

    def __str__(self) -> str:
        return "Alumni [{}]".format(self.fullName)

    # all the related fields
    address: Address
    social: SocialMedia
    jacobs: JacobsData
    approval: Approval
    skills: Skills
    setup: SetupCompleted
    atlas: AtlasSettings
    membership: MembershipInformation


@Alumni.register_component(0)
class Address(AlumniComponentMixin, models.Model):
    """ The address of an Alumni Member """

    member: Alumni = models.OneToOneField(
        Alumni, related_name='address', on_delete=models.CASCADE)

    def is_filled(self) -> bool:
        """ Checks if the user has filled out this component """

        return (self.address_line_1) and (self.city) and (self.zip) and (self.country)

    address_line_1: str = models.CharField(max_length=255, blank=True, null=True,
                                           help_text="E.g. Campus Ring 1")
    address_line_2: Optional[str] = models.CharField(max_length=255, blank=True, null=True,
                                                     help_text="E.g. Apt 007 (optional)")
    city: str = models.CharField(
        max_length=255, blank=True, null=True, help_text="E.g. Bremen")
    zip: str = models.CharField(
        max_length=255, help_text="E.g. 28759", blank=True, null=True)
    state: Optional[str] = models.CharField(max_length=255, blank=True, null=True,
                                            help_text="E.g. Bremen (optional)")
    country: Country = fields.CountryField(blank=True, null=True)

    @property
    def coords(self, default: Optional[Union[List[float], List[None]]] = None) -> Union[List[float], List[None]]:
        """ The coordinates of this user """
        from atlas.models import GeoLocation
        lat, lng = GeoLocation.getLoc(self.country, self.zip)
        if lat is None or lng is None:
            return [None, None]
        else:
            return [lat, lng]

    @classmethod
    def all_valid_coords(cls) -> Iterable[List[float]]:
        """ Returns the coordinates of all alumni """
        coords = map(lambda x: x.coords, cls.objects.filter(
            member__atlas__included=True, member__approval__approval=True))
        return filter(lambda c: c[0] is not None and c[1] is not None, coords)

    @property
    def envelope_format(self):
        if not self.is_filled:
            return None

        lines = [self.address_line_1]

        if self.address_line_2:
            lines.append(self.address_line_2)

        lines.append(f"{self.zip} {self.city}")
        lines.append(f"{self.country.name}")

        return "\n".join(lines)

@Alumni.register_component(1)
class SocialMedia(AlumniComponentMixin, models.Model):
    """ The social media data of a Jacobs Alumni """

    member: Alumni = models.OneToOneField(
        Alumni, related_name='social', on_delete=models.CASCADE)

    facebook: Optional[str] = models.URLField(null=True, blank=True,
                                              help_text="Your Facebook Profile (optional)")
    linkedin: Optional[str] = models.URLField(null=True, blank=True,
                                              help_text="Your LinkedIn Profile (optional)")
    twitter: Optional[str] = models.URLField(null=True, blank=True,
                                             help_text="Your Twitter Account (optional)")
    instagram: Optional[str] = models.URLField(null=True, blank=True,
                                               help_text="Your Instagram (optional)")
    homepage: Optional[str] = models.URLField(null=True, blank=True,
                                              help_text="Your Homepage or Blog")


@Alumni.register_component(2)
class JacobsData(AlumniComponentMixin, models.Model):
    """ The jacobs data of an Alumni Member"""

    member: Alumni = models.OneToOneField(
        Alumni, related_name='jacobs', on_delete=models.CASCADE)

    def is_filled(self) -> bool:
        """ Checks if the user has filled out this component """

        # jacobs data is filled if there is a graduation year and major that aren't "other"
        return (self.graduation != fields.ClassField.OTHER) and (self.major != fields.MajorField.OTHER)

    college: Optional[int] = fields.CollegeField(null=True, blank=True)
    graduation: int = fields.ClassField()
    degree: str = fields.DegreeField(null=True, blank=True)
    major: str = fields.MajorField()
    comments: Optional[str] = models.TextField(null=True, blank=True,
                                               help_text="e.g. exchange semester, several degrees etc.")


class Approval(models.Model):
    """ The approval status of a member """
    member: Alumni = models.OneToOneField(
        Alumni, related_name='approval', on_delete=models.CASCADE)

    approval: bool = models.BooleanField(default=False, blank=True,
                                         help_text="Has the user been approved by an admin?")

    gsuite: Optional[str] = models.EmailField(blank=True, null=True,
                                              help_text="The G-Suite E-Mail of the user", unique=True)

    time: Optional[datetime] = models.DateTimeField(
        null=True, blank=True, help_text="Time the user has been approved")


@Alumni.register_component(3)
class JobInformation(AlumniComponentMixin, models.Model):
    """ The jobs of an Alumni Member"""

    member: Alumni = models.OneToOneField(
        Alumni, related_name='job', on_delete=models.CASCADE)

    employer: Optional[str] = models.CharField(max_length=255, null=True, blank=True,
                                               help_text="Your employer (optional)")
    position: Optional[str] = models.CharField(max_length=255, null=True, blank=True,
                                               help_text="Your position (optional)")
    industry: int = fields.IndustryField()
    job: int = fields.JobField()


@Alumni.register_component(4)
class Skills(AlumniComponentMixin, models.Model):
    """ The skills of an Alumni member """

    member: Alumni = models.OneToOneField(
        Alumni, related_name='skills', on_delete=models.CASCADE)

    otherDegrees: Optional[str] = models.TextField(null=True, blank=True)
    spokenLanguages: Optional[str] = models.TextField(null=True, blank=True)
    programmingLanguages: Optional[str] = models.TextField(
        null=True, blank=True)
    areasOfInterest: Optional[str] = models.TextField(null=True, blank=True,
                                                      help_text="E.g. Start-Ups, Surfing, Big Data, Human Rights, etc")
    alumniMentor: bool = models.BooleanField(default=False, blank=True,
                                             help_text="I would like to sign up as an alumni mentor")


@Alumni.register_component(1000)
class SetupCompleted(AlumniComponentMixin, models.Model):

    member: Alumni = models.OneToOneField(
        Alumni, related_name='setup', on_delete=models.CASCADE)

    date: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return 'Setup Completed On {}'.format(self.date)
