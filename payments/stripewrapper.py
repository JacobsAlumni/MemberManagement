import stripe as stripeapi
from raven.contrib.django.raven_compat.models import client
from datetime import datetime
import time
import pytz


def _safe(operation):
    """ Performs a potentially unsafe operation that interacts with the stripe api """

    result = None

    try:
        result = operation(stripeapi)
    except stripeapi.error.StripeError as e:
        client.captureException()
        return None, e

    return result, None


def _as_safe_operation(f):
    """ Wraps a function with _safe """

    def _wrapper(*args, **kwargs):
        return _safe(lambda stripe: f(stripe, *args, **kwargs))
    return _wrapper


def check_customer_stripe_props(alumni, customer):
    """ Returns a list of errors for the customer """

    header = 'Customer {0!r} (for user {1!r}): '.format(
        customer['id'], alumni.profile.username)

    # errors to be populated
    errors = []

    # Compare fields that aren't identical
    props = _get_stripe_customer_props(alumni)
    for p in props.keys():
        expected = props[p]
        got = customer[p]
        if expected != got:
            errors.append(
                header + "Property {0!r}: Expected {1!r}, but got {2!r}".format(p, expected, got))

    # TODO: Check plan subscription

    # return the errors
    return errors


@_as_safe_operation
def create_customer(stripe, alumni_instance):
    """ Creates a new customer for a given alumni """

    props = _get_stripe_customer_props(alumni_instance)
    customer = stripe.Customer.create(**props)
    return customer.id


@_as_safe_operation
def clear_all_payment_sources(stripe, customer_id):
    """ Removes all payment sources from an alumni """

    for source in stripe.Customer.retrieve(customer_id).sources.list().data:
        # cards can be deleted
        if source.object == 'card':
            source.delete()

        # everything else can be detached
        else:
            source.detach()

    return True


@_as_safe_operation
def update_payment_method(stripe, customer_id, source_id, card_id):
    """ Sets the default payment method for a customer to source or card """

    # clear all existing methods
    cleared, err = clear_all_payment_sources(customer_id)
    if err != None:
        return

    # update the source and card id
    update = {}
    if source_id:
        update['source'] = source_id
    else:
        update['card'] = card_id

    stripe.Customer.modify(customer_id, **update)
    return True


@_as_safe_operation
def create_subscription(stripe, customer_id, plan_id):
    """ Creates a subscription and returns its id """

    subscription = stripe.Customer.retrieve(
        customer_id).subscriptions.create(plan=plan_id)
    return subscription.id


@_as_safe_operation
def update_subscription(stripe, subscription_id, new_plan_id):
    """ Updates the subscription with the given id to the one with the new id """

    subscription = stripe.Subscription.retrieve(subscription_id)
    proration_date = int(time.time())

    stripe.Subscription.modify(
        subscription.id,
        items=[{
            'id': subscription['items']['data'][0].id,
            'plan': new_plan_id,
        }],
        proration_date=proration_date,
    )

    return True


@_as_safe_operation
def get_payment_table(stripe, customer_id):
    """ gets a table of payments for a customer """
    invoices = [_invoice_to_dict(invoice_instance, upcoming=False)
                for invoice_instance in stripe.Invoice.list(customer=customer_id)]

    try:
        upcoming = stripe.Invoice.upcoming(customer=customer_id)
    except stripe.error.InvalidRequestError as e:
        upcoming = None

    if upcoming is not None:
        invoices = [_invoice_to_dict(upcoming, upcoming=True)] + invoices

    return invoices


def _invoice_to_dict(invoice_instance, upcoming):
    """ Turns an invoice instance into a dict for downstream consumption """
    return {
        'lines': [l for l in invoice_instance.lines],
        'date': invoice_instance.date,
        'total': [invoice_instance.total, invoice_instance.currency],
        'upcoming': upcoming,
        'paid': invoice_instance.paid,
        'closed': invoice_instance.closed,
    }


@_as_safe_operation
def get_methods_table(stripe, customer_id):
    """ Gets a list of payment sources for a customer """

    sources = stripe.Customer.retrieve(customer_id).sources.list().data
    return [_source_to_dict(source_instance) for source_instance in sources]


def _source_to_dict(source_instance):
    """ Turns a source instance into a dict for downstream consumption """
    if source_instance.object == 'card':
        return {
            'kind': 'card',
            'brand': source_instance.brand,
            'exp_month': source_instance.exp_month,
            'exp_year': source_instance.exp_year,
            'last4': source_instance.last4
        }
    elif source_instance.type == 'sepa_debit':
        return {
            'kind': 'sepa',
            'last4': source_instance.sepa_debit.last4,
            'mandate_reference': source_instance.sepa_debit.mandate_reference,
            'mandate_url': source_instance.sepa_debit.mandate_url,
        }

    return {'kind': 'unknown'}


@_as_safe_operation
def cancel_subscription(stripe, subscription_id):
    """ Cancels a subscription """

    stripe.Subscription.delete(subscription_id)
    return True


@_as_safe_operation
def get_customer_created(stripe, customer_id):
    """ Gets the time when a customer was created """

    timestamp = stripe.Customer.retrieve(customer_id).created
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

# todo: make api upgrade safe
@_as_safe_operation
def map_customers(stripe, fn):
    """ Calls a function on every customer"""

    # iterate over all the customers
    customers = stripe.Customer.list(limit=100)
    count = 0
    for customer_instance in customers.auto_paging_iter():
        fn(_customer_to_dict(customer_instance))
        count += 1
    return count


def _customer_to_dict(customer_instance):
    """ Turns a stripe customer instance into a dict for downstream consumption """
    return {
        'id': customer_instance.id,
        'description': customer_instance.description,
        'email': customer_instance.email,
    }


@_as_safe_operation
def update_customer(stripe, customer_id, alumni_instance):
    """ Updates a stripe customer with standard properties """
    props = _get_stripe_customer_props(alumni_instance)
    stripe.Customer.modify(customer_id, **props)
    return True


def _get_stripe_customer_props(alumni_instance):
    """ Gets props for a stripe customer given an alumni """

    return {
        'description': 'Alumni Customer for {0!r} ({1!r})'.format(alumni_instance.fullName, alumni_instance.profile.username),
        'email': alumni_instance.email,
    }
