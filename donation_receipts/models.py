import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.core.files.base import ContentFile

from djmoney.models import fields
from django.conf import settings

import pdfrender

from .utils import _convert_to_written

STRIPE = 'stripe'
BANK_ACCOUNT = 'bank'
OTHER = 'other'

# A list of choices for funding sources
_PAYMENT_STREAMS = (
    (STRIPE, 'Stripe'),
    (BANK_ACCOUNT, 'Bank Account'),
    (OTHER, 'Other')
)


# Create your models here.
class DonationReceipt(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False)
    payment_stream = models.CharField(max_length=32, choices=_PAYMENT_STREAMS)
    payment_reference = models.CharField(max_length=256, help_text=_('The unique reference to this payment. \
For bank accounts, use the SEPA transfer ID. For other payment sources, leave a short note.'))

    received_on = models.DateField(help_text=_('The day this donation was received.'))
    issued_on = models.DateField(help_text=_('The day this receipt was issued.'))

    # Decimal(14, 4) is GAAP standard
    amount = fields.MoneyField(max_digits=14, decimal_places=4, default_currency='EUR')

    recipient_info = models.TextField(help_text=_('The full name and postal address of the donation recipient, on multiple lines of text.'))

    receipt_pdf = models.FileField(editable=False)

    def _get_template_context(self):
        return {
            'giant_floating_text': 'MUSTER',
            'address': self.recipient_info,
            'amount_numeric': self.amount,
            'amount_written': _convert_to_written(self.amount),
            'donation_date': self.received_on,
            'receipt_date': self.issued_on,
            'receipt_id': self.external_id
        }

    def _generate_pdf(self):
        context = self._get_template_context()
        context.update({'giant_floating_text': 'MUSTER'})

        f = ContentFile(pdfrender.render_to_bytes(settings.DONATION_RECEIPT_TEMPLATE, context=context))

        self.receipt_pdf.save('receipt-{}.pdf'.format(self.external_id), f)

    def save(self, *args, **kwargs):
        if not self.receipt_pdf:
            self._generate_pdf()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.external_id)
