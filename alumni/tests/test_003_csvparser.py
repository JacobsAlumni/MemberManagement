import unittest

from alumni.utils import CSVParser


class TestCSVParser(unittest.TestCase):
    def __init__(self, *args) -> CSVParser:
        super().__init__(*args)
        self.parser = CSVParser()

        self.parser.register(['ab'], 'ab', lambda ab: ab[0])
        self.parser.register(['a', 'b'], 'ab', lambda ab: ab[0] + ab[1])
        self.parser.register(['c'], 'c', lambda c: c[0])

    def test_simple_fields(self):
        first = self.parser.parse(['a', 'b'], [
            ['a1', 'b1'],
            ['a2', 'b2']
        ])
        self.assertListEqual(
            first, [{'ab': 'a1b1'}, {'ab': 'a2b2'}], 'Parses separate fields correctly')

        second = self.parser.parse(['ab'], [
            ['a1b1'],
            ['a2b2'],
        ])
        self.assertListEqual(
            second, [{'ab': 'a1b1'}, {'ab': 'a2b2'}], 'Parses joint fields correctly')

        third = self.parser.parse(['b', 'a', 'c'], [
            ['b1', 'a1', 'c1'],
            ['b2', 'a2', 'c2']
        ])
        self.assertListEqual(third, [{'ab': 'a1b1', 'c': 'c1'}, {
                             'ab': 'a2b2', 'c': 'c2'}], 'Parses multiple targets correctly')
        
        fourth = self.parser.parse(['', 'b', 'a', 'c', ''], [
            ['x1', 'b1', 'a1', 'c1', 'y1'],
            ['x2', 'b2', 'a2', 'c2', 'y2']
        ])
        self.assertListEqual(fourth, [{'ab': 'a1b1', 'c': 'c1'}, {
                             'ab': 'a2b2', 'c': 'c2'}], 'Can ignore unknown fields')

    def test_required_fields(self):
        first = self.parser.parse(['b', 'a', 'c'], [
            ['b1', 'a1', 'c1'],
            ['b2', 'a2', 'c2']
        ], required=['ab', 'c'])
        self.assertListEqual(first, [{'ab': 'a1b1', 'c': 'c1'}, {
                             'ab': 'a2b2', 'c': 'c2'}], 'Parses required fields correctly')

        with self.assertRaises(Exception, msg="Does not parse when required field is missing"):
            self.parser.parse(['b', 'a'], [
                ['b1', 'a1'],
                ['b2', 'a2']
            ], required=['ab', 'c'])

    def test_wrong_length(self):
        with self.assertRaises(Exception, msg="Does not parse when length is incorrect"):
            self.parser.parse(['b', 'a'], [
                ['b1'],  # missing field
                ['b2', 'a2']
            ])

    def test_unknown_field(self):
        with self.assertRaises(Exception, msg="Does not parse unknown field"):
            self.parser.parse(['bc'], [
                ['b1c1'],
                ['b2c2'],
            ])
