from django.core.management.base import BaseCommand
from atlas.models import GeoLocation

import time

class Command(BaseCommand):
    help = 'Updates Address GeoLocation caches using export of geonames.org'
    # To use: Download and extract https://download.geonames.org/export/zip/allCountries.zip
    # Then run 'python manage.py geocache /path/to/allCountries.txt'

    def add_arguments(self, parser):
        parser.add_argument('fn', help='geonames.org-downloaded file to pull data from')

    def handle(self, *args, **options):
        
        # a new set of locations
        data = []
        contained = set()

        now = time.time()

        # get a list of objects to create
        with open(options['fn']) as f:
            for line in f:
                fields = line.split('\t')

                try:
                    country = fields[0]
                    zip = GeoLocation.normalize_zip(fields[1], fields[0])

                    lat = float(fields[9])
                    lon = float(fields[10])
                except Exception as e:
                    continue
                
                
                if (country, zip) in contained:
                    continue
                else:
                    contained.add((country, zip))
                
                
                data.append(GeoLocation(country = country, zip = zip, lat = lat, lon = lon))
        
        print("Read {} different (country, zip) combinations in {} seconds. ".format(len(data), time.time() - now))
        
        now = time.time()
        GeoLocation.updateData(data)
        print("Updated database in {} seconds. ".format(len(data), time.time() - now))
