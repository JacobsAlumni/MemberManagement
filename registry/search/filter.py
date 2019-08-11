import PreJsPy
import functools

from . import operators as ops


class SearchFilter(object):
    def __init__(self, field_map, plain_search_fields):
        self.parser = PreJsPy.PreJsPy()
        self.parser.setTertiaryOperatorEnabled(False)
        self.parser.setUnaryOperators([
            'not', '!', '~'
        ])
        self.parser.setBinaryOperators({
            # LOGICAL CONNECTIVES
            'and': 1, '&': 1, '&&': 1, '*': 1,
            'or': 1, '|': 1, '||': 1, '+': 1,
            'nand': 1, '!&': 1,
            'xor': 1, '^': 1,

            # Filters
            'equals': 2, ':': 2, '=': 2, '==': 2, '===': 2,
            'less than': 2, '<': 2,
            'less than or equal': 2, '<=': 2, '=<': 2,
            'greater than': 2, '>': 2,
            'greater than or equal': 2, '>=': 2, '=>': 2,
            'contains': 2, '::': 2,
            'matches': 2, 'unicorn': 2, '@': 2,
        })

        self.builder = QueryBuilder(field_map, plain_search_fields)

    def __call__(self, queryset, query):
        try:
            parsed = self.parser.parse(query)
        except Exception as e:
            return None, ParsingError('Unable to understand search', e)

        try:
            q = self.builder(parsed)
        except ParsingError as p:
            return None, p
        except Exception as e:
            return None, ParsingError(str(e), e)

        return q, None


class QueryBuilder(object):
    """Generates a Django Q object from a PreJSPy filter JSON object"""

    def __init__(self, field_map, plain_search_fields):
        self.ops = ops.get_operators(field_map)
        self.fields = plain_search_fields

    def __call__(self, filter_obj):
        return self.translate(filter_obj, finalize=True)

    def translate(self, filter_obj, finalize=False):
        if not filter_obj:
            raise ValueError("Filter was empty")

        # Get filter type
        try:
            obj_type = filter_obj['type']
        except KeyError:
            raise ValueError("Filter has no type")

        # Decide what to do based on filter type
        if obj_type == ops.BIN_TYPE:
            res = self._generate_binary(filter_obj)

        elif obj_type == ops.UN_TYPE:
            res = self._generate_unary(filter_obj)

        elif obj_type == ops.COMPOUND_TYPE:
            res = self._generate_compound(filter_obj)

        elif obj_type in [ops.IDENTITY_TYPE, ops.STRING_TYPE]:
            res = self._generate_literal(filter_obj)

        else:
            raise NotImplementedError("Invalid filter type: " + obj_type)

        if finalize and (isinstance(res, str) or isinstance(res, float)):
            res = self._finalize(str(res))

        return res

    def _generate_binary(self, filter_obj):
        try:
            left = filter_obj['left']
            right = filter_obj['right']
            filter_type = filter_obj['operator']
        except KeyError as e:
            raise ValueError("Binary is incomplete: " + str(e))

        try:
            op = self.ops['BIN_OPS'][filter_type]
        except KeyError as k:
            raise ParsingError(
                'Unknown binary operator {}'.format(filter_type), k)
        except TypeError as t:
            raise ParsingError('Cannot use binary operator {} on {} and {}'.format(
                filter_type, left, right))

        return op(self.translate(left), self.translate(right))

    def _generate_unary(self, filter_obj):
        try:
            argument = filter_obj['argument']
            filter_type = filter_obj['operator']
        except KeyError as e:
            raise ValueError("Unary is missing: " + str(e))

        try:
            op = self.ops['UNARY_OPS'][filter_type]
        except KeyError as k:
            raise ParsingError(
                'Unknown unary operator {}'.format(filter_type), k)
        except TypeError as t:
            raise ParsingError(
                'Cannot use unary operator {} on {}'.format(filter_type, argument))

        return op(self.translate(argument))

    def _generate_compound(self, filter_obj):
        """Compound expressions are implicitly converted into a series of
        AND connected clauses."""

        try:
            body = filter_obj['body']
        except KeyError as e:
            raise ValueError("Compound is missing: " + str(e))

        clauses = [self.translate(part, finalize=True) for part in body]

        if len(clauses) == 0:
            raise ValueError('Empty search')

        return functools.reduce(self.ops['and_fn'], clauses)

    def _generate_literal(self, literal):
        try:
            if literal['type'] == ops.IDENTITY_TYPE:
                return literal['name']
            elif literal['type'] == ops.STRING_TYPE:
                return literal['value']
            else:
                raise NotImplementedError
        except KeyError as e:
            raise ValueError("Invalid literal: " + str(e))

    def _finalize(self, s):
        """ Generates a string search """
        return ops.build_text_search(s, self.fields)


class ParsingError(Exception):
    def __init__(self, message, caused_by):
        super().__init__(message)
        self.message = message
        self.caused_by = caused_by
