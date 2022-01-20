from __future__ import annotations

import os.path
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

LOCAL_SETTINGS_PATH = os.path.normpath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'local_settings.py'))

LOCAL_SETTINGS_TEMPLATE = """
# automatically generated local_settings.py
import os

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")

GSUITE_AUTH_FILE = os.environ.get("GSUITE_AUTH_FILE")
"""


class Command(BaseCommand):
    help = 'Create a template local_settings.py'

    def handle(self, *args, **kwargs) -> None:
        if not settings.DEBUG:
            print("Refusing to work outside of DEBUG mode")
            sys.exit(1)

        if os.path.exists(LOCAL_SETTINGS_PATH):
            print("{} already exists, nothing to do. ".format(LOCAL_SETTINGS_PATH))
            return

        with open(LOCAL_SETTINGS_PATH, 'w') as f:
            f.write(LOCAL_SETTINGS_TEMPLATE)

        print("Wrote {}".format(LOCAL_SETTINGS_PATH))
        print("You probably want to customize it")
