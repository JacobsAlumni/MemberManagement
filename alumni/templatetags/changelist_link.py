from urllib.parse import urlencode
from django.template import Library
from django.urls import reverse
from urllib.parse import parse_qsl

from typing import List

register = Library()


@register.simple_tag(takes_context=True)
def changelist_link(context, filter: str, value: str) -> str:
    opts = context.get('opts')
    preserved_filters = context.get('preserved_filters')

    query = dict()

    # extract query from the url!
    if preserved_filters:
        query = dict(parse_qsl(preserved_filters))
        if '_changelist_filters' in query:
            query = dict(parse_qsl(query['_changelist_filters']))

    # update the query
    query[filter] = value

    # and make a changelist link!
    return reverse('admin:{}_{}_changelist'.format(opts.app_label, opts.model_name)) + '?' + urlencode(query)

@register.simple_tag(takes_context=True)
def changelist_search(context, *values: List[str]) -> str:
    opts = context.get('opts')

    query = ' '.join(filter(lambda x: x, values))
    return reverse('admin:{}_{}_changelist'.format(opts.app_label, opts.model_name)) + '?' + urlencode({'q': query})
