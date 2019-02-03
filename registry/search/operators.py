import operator
from django.db import models

import functools

"""This module holds all the logical and non-logical operators and static
definitions used in QBuilder."""

def build_text_search(text, fields):
    """ Builds a query object from a string and the given search fields """

    # This code has been adapted from Django Admin
    # and just mangles search fields

    # contruct the field searches
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name
    
    # generate searches for each field
    orm_lookups = [construct_search(str(search_field)) for search_field in fields]

    # the total searches
    searches = []

    # split the text into bits
    for bit in text.split():
        or_queries = [models.Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
        bitsearch = functools.reduce(operator.or_, or_queries)
        searches.append(bitsearch)
    
    return functools.reduce(operator.and_, searches)

def get_operators(field_map):
    """ Gets implementations of operators """

    # Binary logic expressions
    and_fn = operator.and_
    or_fn = operator.or_

    not_fn = operator.invert

    xor_fn = lambda x, y: or_fn(and_fn(not_fn(x), y), and_fn(x, not_fn(y)))
    nand_fn = lambda x, y: not_fn(and_fn(x, y))

    def q_lambda(dj_filter="exact"):
        def impl(x, y):
            return models.Q(**{field_map[x] + '__' + dj_filter: y})
        return impl 


    def not_eq(x, y):
        return not_fn(q_lambda()(x, y))

    UNARY_OPS = {
        'not': not_fn,
        '!': not_fn,
        '~': not_fn
    }

    BIN_OPS = {
        # LOGICAL CONNECTIVES
        'and': and_fn, '&': and_fn, '&&': and_fn, '*': and_fn,

        'or': or_fn, '|': or_fn, '||': or_fn, '+': or_fn,

        'nand': nand_fn, '!&': nand_fn,

        'xor': xor_fn, '^': xor_fn,

        # FILTERS
        'equals': q_lambda(),
        'eq': q_lambda(),
        ':': q_lambda(),
        '=': q_lambda(),
        '==': q_lambda(),
        '===': q_lambda(),

        '!=': not_eq,

        'less than': q_lambda('lt'),
        '<': q_lambda('lt'),

        'less than or equal': q_lambda('lte'),
        '<=': q_lambda('lte'),
        '=<': q_lambda('lte'),

        'greater than': q_lambda('gt'),
        '>': q_lambda('gt'),

        'greater than or equal': q_lambda('gte'),
        '>=': q_lambda('gte'),
        '=>': q_lambda('gte'),

        'contains': q_lambda('icontains'),
        '::': q_lambda('icontains'),

        'matches': q_lambda('regex'),
        'unicorn': q_lambda('regex'),
        '@': q_lambda('regex')
    }

    return {
        'and_fn': and_fn,
        'UNARY_OPS': UNARY_OPS,
        'BIN_OPS': BIN_OPS,
    }

COMPOUND_TYPE = 'Compound'
BIN_TYPE = 'BinaryExpression'
UN_TYPE = 'UnaryExpression'
IDENTITY_TYPE = 'Identifier'
STRING_TYPE = 'Literal'
