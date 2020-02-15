import stripe as stripeapi
from raven.contrib.django.raven_compat.models import client


def safe(operation):
    """ Safely performs an operation with the stripe API """

    result = None

    try:
        result = operation(stripeapi)
    except stripeapi.error.StripeError as e:
        client.captureException()
        return None, e

    return result, None


def as_safe_operation(f):
    """ A decorator to turn a function into a safe operation """

    def _wrapper(*args, **kwargs):
        return safe(lambda stripe: f(stripe, *args, **kwargs))
    return _wrapper


def get_stripe_customer_props(alumni):
    """ Gets props for a stripe customer given an alumni """

    return {
        'description': 'Alumni Customer for {0!r} ({1!r})'.format(alumni.fullName, alumni.profile.username),
        'email': alumni.email,
    }


def check_customer_stripe_props(alumni, customer):
    """ Returns a list of errors for the customer """

    header = 'Customer {0!r} (for user {1!r}): '.format(
        customer.id, alumni.profile.username)

    # errors to be populated
    errors = []

    # Compare fields that aren't identical
    props = get_stripe_customer_props(alumni)
    for p in props.keys():
        expected = props[p]
        got = getattr(customer, p)
        if expected != got:
            errors.append(
                header + "Property {0!r}: Expected {1!r}, but got {2!r}".format(p, expected, got))

    # TODO: Check plan subscription

    # return the errors
    return errors


@as_safe_operation
def create_customer(stripe, alumni):
    """ Creates a customer for the given alumni """

    props = get_stripe_customer_props(alumni)
    return stripe.Customer.create(**props)


@as_safe_operation
def update_customer(stripe, customer, alumni):
    props = get_stripe_customer_props(alumni)
    return stripe.Customer.modify(customer, **props)


@as_safe_operation
def clear_all_payment_sources(stripe, customer):
    """ Removes all payment sources from an alumni """

    for source in stripe.Customer.retrieve(customer).sources.list().data:
        # cards can be deleted
        if source.object == 'card':
            source.delete()

        # everything else can be detached
        else:
            source.detach()

    return True


@as_safe_operation
def update_payment_method(stripe, customer, source, card):
    """ Sets the default payment method for a customer to source or card """

    # clear all existing methods
    cleared, err = clear_all_payment_sources(customer)
    if err != None:
        return

    # update the source and card id
    update = {}
    if source:
        update['source'] = source
    else:
        update['card'] = card

    return stripe.Customer.modify(customer, **update)


@as_safe_operation
def create_subscription(stripe, customer, plan):
    """ Creates a subscription for the customer """

    # Creates a new subscription for the customer
    return stripe.Customer.retrieve(customer).subscriptions.create(plan=plan)


@as_safe_operation
def get_payment_table(stripe, customer):
    """ gets a table of payments for a customer """
    return [{
        'lines': [l for l in iv.lines],
        'date': iv.date,
        'total': [iv.total, iv.currency],
        'paid': iv.paid,
        'closed': iv.closed
    } for iv in stripe.Invoice.list(customer=customer)]


@as_safe_operation
def get_methods_table(stripe, customer):
    def format_source(source):
        if source.object == 'card':
            return {
                'kind': 'card',
                'brand': source.brand,
                'exp_month': source.exp_month,
                'exp_year': source.exp_year,
                'last4': source.last4
            }
        elif source.type == 'sepa_debit':
            return {
                'kind': 'sepa',
                'last4': source.sepa_debit.last4,
                'mandate_reference': source.sepa_debit.mandate_reference,
                'mandate_url': source.sepa_debit.mandate_url,
            }

        return {'kind': 'unknown'}

    return [format_source(source) for source in stripe.Customer.retrieve(customer).sources.list().data]


@as_safe_operation
def cancel_subscription(stripe, subscription):
    """ Cancels a subscription """

    # cancel the subscription
    return stripe.Subscription.delete(subscription)


@as_safe_operation
def map_customers(stripe, fn):
    """ Gets a list containing all customer ids """

    # iterate over all the customers
    customers = stripe.Customer.list(limit=100)
    for customer in customers.auto_paging_iter():
        fn(customer)
