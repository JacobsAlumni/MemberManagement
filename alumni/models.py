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

    email = models.EmailField(help_text="Your private email address")

    # gender, nationality, birthday
    sex = fields.GenderField()
    birthday = models.DateField(help_text="Your birthday in the format YYYY-MM-DD")

    # TODO: Better handling of multiple nationalities
    nationality = CountryField(help_text="Your nationality", multiple=True)

    # kind
    category = fields.AlumniCategoryField()

    def get_first_unset_approval(self):
        """ Gets the first unset component or returns None if it already exists. """

        # Get the approval object
        try:
            approval = self.approval
        except ObjectDoesNotExist:
            approval = None

        # Create it if it doesn't exist
        if approval is None:
            approval = Approval.objects.create(member=self)
            approval.save()

        return approval.get_first_unset()




    def __str__(self):
        return "Alumni [{} {} {}]".format(self.firstName, self.middleName, self.lastName)


class Approval(models.Model):
    """ The approval status of a member """
    member = models.OneToOneField(Alumni, related_name='approval')

    approval = models.BooleanField(default=False,
                                   help_text="Has the user been approved by an admin?")

    def set_address(self):
        """ Checks if this member has inputted an address """
        try:
            _ = self.member.address
            return True
        except ObjectDoesNotExist:
            return False

    def set_jacobs(self):
        """ Checks if this member has inputted Jacobs Data """
        try:
            _ = self.member.jacobs
            return True
        except ObjectDoesNotExist:
            return False

    def set_social(self):
        """ Checks if this member has inputted Social Media Information """
        try:
            _ = self.member.social
            return True
        except ObjectDoesNotExist:
            return False

    def set_job(self):
        """ Checks if this member has inputted a Job """
        try:
            _ = self.member.job
            return True
        except ObjectDoesNotExist:
            return False

    def get_first_unset(self):
        """ Gets a string of the first unset item or None"""

        if not self.set_address():
            return 'address'

        if not self.set_jacobs():
            return 'jacobs'

        if not self.set_social():
            return 'social'

        if not self.set_social():
            return 'job'

        return None


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


class JacobsData(models.Model):
    """ The jacobs data of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='jacobs')

    college = fields.CollegeField(null=True, blank=True)
    graduation = fields.ClassField()
    degree = fields.DegreeField(null=True, blank=True)
    major = fields.MajorField()


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


class JobInformation(models.Model):
    """ The jobs of an Alumni Member"""

    member = models.OneToOneField(Alumni, related_name='job')

    employer = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your employer (optional)")
    position = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your position (optional)")
    industry = fields.IndustryField()
    job = fields.JobField()
