from __future__ import annotations

import warnings
import re

from django.db import models, transaction

from alumni.models import Alumni
from alumni.fields import CountryField

from registry.alumni import AlumniComponentMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List, Dict, Any
    from django_countries.fields import Country


@Alumni.register_component(5)
class AtlasSettings(AlumniComponentMixin, models.Model):
    member: Alumni = models.OneToOneField(
        Alumni, related_name='atlas', on_delete=models.CASCADE)

    included: bool = models.BooleanField(default=False, blank=True,
                                         help_text="Include me in the Alumni Atlas. By selecting this checkbox, your location (approximated by your zip code), your city, and other information about you will be visible on the atlas interface to other users. ")

    birthdayVisible: bool = models.BooleanField(
        default=False, blank=True, help_text="Show Birthday on my Alumni Atlas Profile")

    contactInfoVisible: bool = models.BooleanField(
        default=False, blank=True, help_text="Show Social Media and Contact information (like @jacobs-alumni email) on the Alumni Atlas Profile Page. ")

    secret: Optional[str] = models.TextField(
        null=True, blank=True, help_text='Secret Search Text that the member can be found with')


class GeoLocation(models.Model):
    """ Represents a (cached) GeoLocation """

    country: Country = CountryField()
    zip: str = models.CharField(max_length=10)

    lat: float = models.FloatField()
    lon: float = models.FloatField()

    class Meta:
        unique_together = (('country', 'zip'))

    @classmethod
    def getLocInstance(cls, country: str, zip: str) -> Optional[GeoLocation]:
        try:
            return cls.objects.get(
                country=country, zip=cls.normalize_zip(zip, country.code))
        except cls.DoesNotExist:
            #warnings.warn('No location for combination: {} {}'.format(
            #    country.code, cls.normalize_zip(zip, country.code)))
            return None

    @classmethod
    def getLoc(cls, country: str, zip: str) -> Union[Tuple[float, float], Tuple[None, None]]:
        instance = cls.getLocInstance(country, zip)
        if instance is None:
            return None, None
        return instance.lat, instance.lon

    @classmethod
    def updateData(cls, data: List[Dict[str, Any]]):
        with transaction.atomic():
            cls.objects.all().delete()
            cls.objects.bulk_create(data)

    @classmethod
    def normalize_zip(self, zip: str, country: str) -> str:
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

    def __str__(self) -> str:
        return 'GeoLocation of {} in {}'.format(self.zip, self.country)
