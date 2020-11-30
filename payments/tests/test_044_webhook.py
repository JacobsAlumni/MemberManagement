import json

from django.test import TestCase
from django.shortcuts import reverse

from unittest import mock

from ..models import PaymentIntent

SAMPLE_WEBHOOK_EVENT = {
  "object": {
    "id": "pi_1HoqahK8wO5tRpJk6naUgArH",
    "object": "payment_intent",
    "allowed_source_types": [
      "card"
    ],
    "amount": 3900,
    "amount_capturable": 0,
    "amount_received": 0,
    "application": None,
    "application_fee_amount": None,
    "canceled_at": None,
    "cancellation_reason": None,
    "capture_method": "automatic",
    "charges": {
      "object": "list",
      "data": [
      ],
      "has_more": False,
      "total_count": 0,
      "url": "/v1/charges?payment_intent=pi_1HoqahK8wO5tRpJk6naUgArH"
    },
    "client_secret": "pi_1HoqahK8wO5tRpJk6naUgArH_secret_nDUkMXNAcMVILRc5Isk4U1NSp",
    "confirmation_method": "automatic",
    "created": 1605705655,
    "currency": "eur",
    "customer": "cus_IPfjXUhMspR8Mc",
    "description": "Subscription creation",
    "invoice": None,
    "last_payment_error": None,
    "livemode": False,
    "metadata": {
    },
    "next_action": None,
    "next_source_action": None,
    "on_behalf_of": None,
    "payment_method": None,
    "payment_method_options": {
      "card": {
        "installments": None,
        "network": None,
        "request_three_d_secure": "automatic"
      }
    },
    "payment_method_types": [
      "card"
    ],
    "receipt_email": None,
    "review": None,
    "setup_future_usage": "off_session",
    "shipping": None,
    "source": None,
    "statement_descriptor": "JACOBSALUMNI",
    "statement_descriptor_suffix": None,
    "status": "requires_source",
    "transfer_data": None,
    "transfer_group": None
  }
}

LOADED_EVENT_DATA = {
        'id': SAMPLE_WEBHOOK_EVENT['object']['id'],
        'created': SAMPLE_WEBHOOK_EVENT['object']['created'],
        'customer': SAMPLE_WEBHOOK_EVENT['object']['customer'],
        'amount': SAMPLE_WEBHOOK_EVENT['object']['amount'],
        'amount_capturable': SAMPLE_WEBHOOK_EVENT['object']['amount_capturable'],
        'amount_received': SAMPLE_WEBHOOK_EVENT['object']['amount_received'],
        'status': SAMPLE_WEBHOOK_EVENT['object']['status'],
        'currency': SAMPLE_WEBHOOK_EVENT['object']['currency']
}

class AttribMock:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def _stripe_mock(payload, *args):
    return (AttribMock({'type': 'payment_intent.mock', 'data': AttribMock({'object': AttribMock(json.loads(payload)['object'])})}), None)

class WebhookTest(TestCase):
    def test_rejects_unsigned(self):
        response = self.client.post(reverse('webhook'), data=SAMPLE_WEBHOOK_EVENT, content_type='application/json', HTTP_STRIPE_SIGNATURE='utter garbage')
        self.assertEqual(response.status_code, 400)

    # Patch out the Stripe signature verification
    @mock.patch('payments.stripewrapper.make_stripe_event', _stripe_mock)
    def test_accepts_event(self):
        response = self.client.post(reverse('webhook'), data=SAMPLE_WEBHOOK_EVENT, content_type='application/json', HTTP_STRIPE_SIGNATURE='utter garbage')

        self.assertEqual(response.status_code, 200)

    # Patch out the Stripe signature verification
    @mock.patch('payments.stripewrapper.make_stripe_event', _stripe_mock)
    def test_creates_local_object(self):
        response = self.client.post(reverse('webhook'), data=SAMPLE_WEBHOOK_EVENT, content_type='application/json')

        self.assertTrue(PaymentIntent.objects.filter(stripe_id=SAMPLE_WEBHOOK_EVENT['object']['id']).exists())

    # Patch out the Stripe signature verification
    @mock.patch('payments.stripewrapper.make_stripe_event', _stripe_mock)
    def test_loads_event_data(self):
        response = self.client.post(reverse('webhook'), data=SAMPLE_WEBHOOK_EVENT, content_type='application/json')

        local_pi = PaymentIntent.objects.filter(stripe_id=SAMPLE_WEBHOOK_EVENT['object']['id']).first()

        self.assertDictEqual(local_pi.data, LOADED_EVENT_DATA)
