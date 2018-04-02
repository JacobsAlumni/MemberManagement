import stripe
from django.conf import settings
from django.shortcuts import render
from raven.contrib.django.raven_compat.models import client

from registry.decorators import require_setup_completed
from registry.views.registry import default_alternative

from datetime import datetime
from django.utils import formats


def format_date(epoch):
    """ Formats seconds since epoch as a readable date """

    date_joined = datetime.fromtimestamp(epoch)
    return formats.date_format(date_joined, "DATETIME_FORMAT")


def format_total(amount, cur):
    """ Formats the total """
    if cur == "eur":
        return "%0.2f €" % (amount / 100)
    elif cur == "usd":
        return "%0.2f $" % (amount / 100)
    else:
        raise Exception("unknown currency {}".format(cur))


def get_invoice_table(customer_id):
    error = None
    invoices = []

    if customer_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            for iv in stripe.Invoice.list(customer=customer_id):
                invoices.append({
                    'description': [l.description for l in stripe.Invoice.retrieve(iv.id).lines.all()],
                    'date': format_date(iv.date),
                    'total': format_total(iv.total, iv.currency),
                    'paid': iv.paid,
                    'closed': iv.closed
                })
        except stripe.error.RateLimitError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.RateLimitError). " \
                    "Please try again later or contact support. "
        except stripe.error.InvalidRequestError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.InvalidRequestError). " \
                    "Please try again later or contact support. "
        except stripe.error.AuthenticationError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.AuthenticationError). " \
                    "Please try again later or contact support. "
        except stripe.error.APIConnectionError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.APIConnectionError). " \
                    "Please try again later or contact support. "
        except stripe.error.StripeError as e:
            client.captureException()
            error = "Something went wrong trying to retrieve your payments. " \
                    "Please try again later or contact support. "
        except Exception as e:
            client.captureException()
            error = "Something went wrong trying to retrieve your payments. " \
                    "Please try again later or contact support. "
    else:
        error = "Something went wrong (missing Customer ID). " \
                "Please contact support or try again later. "

    return (error, invoices)


@require_setup_completed(default_alternative)
def payments(request):
    (error, invoices) = get_invoice_table(request.user.alumni.payment.customer)

    return render(request, 'payments/view.html', {
        'invoices': invoices,
        'error': error
    })
