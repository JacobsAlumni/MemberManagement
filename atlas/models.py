import warnings
import re

from django.db import models, transaction

from alumni.models import Alumni
from alumni.fields import CountryField

from registry.alumni import AlumniComponentMixin

@Alumni.register_component(5)
class AtlasSettings(AlumniComponentMixin, models.Model):
    member = models.OneToOneField(Alumni, related_name='atlas', on_delete=models.CASCADE)

    included = models.BooleanField(default=False, blank=True,
                                         help_text="Include me in the Alumni Atlas. By selecting this checkbox, your location (approximated by your zip code), your city, and other information about you will be visible on the atlas interface to other users. ")

    birthdayVisible = models.BooleanField(default=False, blank=True, help_text="Show Birthday on my Alumni Atlas Profile")

    contactInfoVisible = models.BooleanField(default=False, blank=True, help_text="Show Social Media and Contact information (like @jacobs-alumni email) on the Alumni Atlas Profile Page. ")

    secret = models.TextField(null=True, blank=True, help_text='Secret Search Text that the member can be found with')

class GeoLocation(models.Model):
    """ Represents a (cached) GeoLocation """

    country = CountryField()
    zip = models.CharField(max_length=10)

    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        unique_together = (('country', 'zip'))
        
    @classmethod
    def getLoc(cls, country, zip):
        try:
            instance = cls.objects.get(country=country, zip=cls.normalize_zip(zip, country.code))
        except cls.DoesNotExist:
            warnings.warn('No location for combination: {} {}'.format(country.code, cls.normalize_zip(zip, country.code)))
            return None, None
        
        return instance.lat, instance.lon
    
    @classmethod
    def updateData(cls, data):
        with transaction.atomic():
            cls.objects.all().delete()
            cls.objects.bulk_create(data)
    
    @classmethod
    def normalize_zip(self, zip, country):
        lowerzip = zip.lower()
        norm = re.sub(r'[^0-9a-z]', '', lowerzip)

        # Canada: First three characters
        if country == 'CA':
            norm = norm[0:3]
        # Great Briatin: First four characters
        elif country == 'GB':
            norm = norm[0:4]
        # Netherlands: digits only
        elif country == 'NL':
            norm = re.sub(r'[^0-9]', '', norm)
        return norm
    
    def __str__(self):
        return 'GeoLocation of {} in {}'.format(self.zip, self.country)