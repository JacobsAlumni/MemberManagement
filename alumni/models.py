from django.db import models
from django.contrib import admin

from django_countries.fields import CountryField
from . import fields


class AlumniMember(models.Model):
    # name and basic contact information
    firstName = models.CharField(max_length=255, help_text="Your first name")
    middleName = models.CharField(max_length=255, blank=True, null=True,
                                  help_text="Your middle names (optional)")
    lastName = models.CharField(max_length=255, help_text="Your last name")

    email = models.EmailField(help_text="Your private email address")

    # gender, nationality, birthday
    sex = fields.GenderField()
    birthday = models.DateField(help_text="Your birthday")

    # TODO: Better handling of multiple nationalities
    nationality = CountryField(help_text="Your nationality", multiple=True)

    # kind
    category = fields.AlumniCategoryField()

    # address
    address_line_1 = models.CharField(max_length=255,
                                      help_text="E.g. Campus Ring 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="E.g. Apt 007 (optional)")
    city = models.CharField(max_length=255, help_text="E.g. Bremen")
    zip = models.CharField(max_length=255, help_text="E.g. 28759")
    state = models.CharField(max_length=255, blank=True, null=True,
                             help_text="E.g. Bremen (optional)")
    country = CountryField()

    # social media
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

    # Alumni Data
    college = fields.CollegeField(null=True, blank=True)
    graduation = fields.ClassField()
    degree = fields.DegreeField(null=True, blank=True)
    major = fields.MajorField()

    # Job Info
    employer = models.CharField(max_length=255, null=True, blank=True, help_text="Your employer (optional)")
    position = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Your position (optional)")
    industry = fields.IndustryField()
    job = fields.JobField()


    def __str__(self):
        return "Alumni[{} {} {}]".format(self.firstName, self.middleName,
                                         self.lastName)

class AlumniAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlumniMember, AlumniAdmin)
