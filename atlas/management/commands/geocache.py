import io
import time
import zipfile
from contextlib import closing

import requests
from django.core.management.base import BaseCommand

from atlas.models import GeoLocation

DOWNLOAD_URL = "https://download.geonames.org/export/zip/allCountries.zip"


class Command(BaseCommand):
    help = 'Updates Address GeoLocation caches using export of geonames.org'
    # To use: Download and extract https://download.geonames.org/export/zip/allCountries.zip
    # Then run 'python manage.py geocache /path/to/allCountries.txt'

    def add_arguments(self, parser):
        parser.add_argument(
            'fn', nargs='?', help='Filename to import data from. If omitted, download a fresh file from the internet. ', default=None)

    def handle(self, *args, **options):
        fn = options['fn']
        if not fn:
            self.handle_download()
        else:
            with open(fn, 'r') as f:
                self.handle_file(f)

    def handle_download(self):
        now = time.time()
        print('Downloading {}, this may take a few seconds. '.format(DOWNLOAD_URL))

        r = requests.get(DOWNLOAD_URL)
        with closing(r), zipfile.ZipFile(io.BytesIO(r.content)) as archive:
            return self.handle_file(archive.open('allCountries.txt', 'r'))

    def handle_file(self, f):
        # a new set of locations
        data = []
        contained = set()

        now = time.time()

        # get a list of objects to create
        for line in f.readlines():
            # decode the line if
            try:
                line = line.decode('utf-8')
            except:
                pass

            # split into fields
            fields = line.split('\t')

            # get the important fields
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

            data.append(GeoLocation(country=country,
                                    zip=zip, lat=lat, lon=lon))

        # and we're done reading, now write to the database
        print("Read {} different (country, zip) combinations in {} seconds. ".format(
            len(data), time.time() - now))

        now = time.time()
        GeoLocation.updateData(data)
        print("Updated database in {} seconds. ".format(time.time() - now))
