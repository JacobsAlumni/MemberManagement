import io
import sys
import time
import zipfile

import requests
from urllib.request import urlopen
from django.core.management.base import BaseCommand
from tqdm import tqdm

from atlas.models import GeoLocation

# Using our own mirror to not abuse geonames.org bandwidth too much
# DOWNLOAD_URL = "https://download.geonames.org/export/zip/allCountries.zip"
DOWNLOAD_URL = "https://github.com/JacobsAlumni/geonames.org-mirror/releases/download/v2020.01/allCountries.zip"

class Command(BaseCommand):
    help = 'Updates Address GeoLocation caches using export of geonames.org'

    def add_arguments(self, parser):
        parser.add_argument(
            'fn', nargs='?', help='Filename to import data from. If omitted, download a fresh file from the internet. ', default=None)
        parser.add_argument(
            '--url', default=DOWNLOAD_URL, help='URL to download zipped data from. '
        )

    def handle(self, *args, **options):
        fn = options['fn']
        if not fn:
            self.handle_download(options['url'])
        else:
            with open(fn, 'r') as f:
                self.handle_file(f)

    def handle_download(self, url):
        now = time.time()

        # download into memory
        print('Downloading from {}. '.format(url))
        data = self._fetch_with_tqdm(url)

        # open the archive
        with zipfile.ZipFile(data) as archive:
            return self.handle_file(archive.open('allCountries.txt', 'r'))

    def _fetch_with_tqdm(self, url):
        """ Fetchs a URL with requests and tqdm. Returns a BytesIO """

        # grab the total file size and create an appropriate bar
        file_size = int(urlopen(url).info().get('Content-Length', -1))
        pbar = tqdm(total=file_size, unit='B',
                    unit_scale=True, desc="Downloading")

        # create a buffer and make the request
        buffer = io.BytesIO()
        req = requests.get(url, stream=True)

        # iterate over the data in chunk of 1024 bytes
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                buffer.write(chunk)
                pbar.update(1024)

        # close the bar and return the buffer
        pbar.close()
        return buffer

    def handle_file(self, f):
        # a new set of locations
        data = []
        contained = set()

        # get a list of objects to create
        for line in tqdm(f.readlines(), desc='Parsing'):
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

        print("Updating database ... ", end='')
        sys.stdout.flush()
        now = time.time()
        GeoLocation.updateData(data)
        print("done in {} seconds. ".format(time.time() - now))
