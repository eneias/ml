'''Tests for the parsing utilities for .tra files.'''

import unittest

from ml.parse_utils import tuplify, unnamespace


class TestParseUtils(unittest.TestCase):
    def test_tuplify_base_case(self):
        s = '"Abcd" = "Defg hij"'
        expected = ('Abcd', 'Defg hij')
        self.assertEqual(tuplify(s), expected)

    def test_tuplify_no_match(self):
        s = '"Abcd" = lack of quotes'
        self.assertIsNone(tuplify(s))

    def test_tuplify_escaped_quote(self):
        s = ('"I have an \\"escaped quote\\"." = '
             '"Eu tenho \\"aspas escapadas\\"."')
        expected = ('I have an \\"escaped quote\\".',
                    'Eu tenho \\"aspas escapadas\\".')
        self.assertEqual(tuplify(s), expected)

    def test_unnamespace(self):
        s = 'Namespace|Very complex string.'
        expected = 'Very complex string.'
        self.assertEqual(unnamespace(s), expected)

if __name__ == '__main__':
    unittest.main()
