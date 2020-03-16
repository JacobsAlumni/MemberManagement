from __future__ import annotations

from django.test import TestCase
from atlas.models import GeoLocation
from django.core import management
import os

class GeoCacheTest(TestCase):
    def test_download(self) -> None:
        if os.environ.get('ENABLE_GEOCACHE_TEST', "0") != "1":
            self.skipTest('Skipping, set ENABLE_GEOCACHE_TEST=1 to enable')

        management.call_command(
            'geocache', url="https://github.com/JacobsAlumni/geonames.org-mirror/releases/download/v2020.01/allCountries.zip")
        self.assertEqual(GeoLocation.objects.count(), 852799,
                         'Correct number of objects received')
