from __future__ import annotations

# Sets up the stripe api key
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
stripe.api_version = "2017-08-15"
