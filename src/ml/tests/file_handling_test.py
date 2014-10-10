"""Tests for the ML file handling module."""

import unittest

from textwrap import dedent
from unittest.mock import MagicMock, Mock

from mock_utils.mock_file import (with_mock_files,
                                  with_mock_file_factories,
                                  make_mock_file)

from ml.file_handling import (read_code,
                              read_list,
                              read_dict,
                              tra_file,
                              read_list_with_fallback)

FILES = {'ok': dedent('''\
         "Abcd" = "Defg hij"
         "XYZ test" = "This should not break."
         '''),
         'breaker': dedent('''\
         "Abcd" = "Defg hij"
         quotes missing = "This should break."
         '''),
         'complete': dedent('''\
         "Test string." = "String de teste."
         "Another test." = "Outro teste."
         "Yet another." = "Ainda outra."
         "Terrible \\"corner case\\"." = "Terrível \\"caso obscuro\\"."
         '''),
         'italian': dedent('''\
         "Test string." = "String di prova."
         "Another test." = ""
         "Yet another." = "Ancora un'altra."
         ''')}

EXPECTED_COMPLETE_LIST = [('Test string.', 'String de teste.'),
                          ('Another test.', 'Outro teste.'),
                          ('Yet another.', 'Ainda outra.'),
                          ('Terrible \\"corner case\\".',
                           'Terrível \\"caso obscuro\\".')]

EXPECTED_LIST_OK = [('Abcd', 'Defg hij'),
                    ('XYZ test', 'This should not break.')]

EXPECTED_DICT_OK = dict(EXPECTED_LIST_OK)


def file_as_lines(filename):
    """Return a mock file text as a list of lines."""
    return FILES[filename].split('\n')


def remove_empty_lines(lines):
    """Remove empty lines from a list."""
    return [line for line in lines if line]


def sort_file(filename):
    """Return a mock file text in sorted order."""
    return '\n'.join(sorted(remove_empty_lines(file_as_lines(filename))))


@with_mock_files(FILES)
class TestFileHandling(unittest.TestCase):
    """Test class for the ML file handling module."""
    def test_read_list_success(self):
        l = read_list(open('ok', 'r'))
        self.assertEqual(l, EXPECTED_LIST_OK)

    def test_read_list_failure(self):
        with self.assertRaises(ValueError):
            read_list(open('breaker', 'r'))

    def test_read_dict_success(self):
        l = read_dict(open('ok', 'r'))
        self.assertEqual(l, EXPECTED_DICT_OK)

    def test_read_dict_failure(self):
        with self.assertRaises(ValueError):
            read_dict(open('breaker', 'r'))

    def test_read_list_with_fallback(self):
        with open('complete', 'r') as file_handler, open('italian', 'r') as fallback:
            l = read_list_with_fallback(file_handler, fallback=fallback)
        self.assertEquals(l, EXPECTED_COMPLETE_LIST)

    def test_tra_file(self):
        sorted_text = sort_file('ok')
        self.assertEqual(tra_file(EXPECTED_LIST_OK), sorted_text)


def make_failing_mock():
    failing_mock = make_mock_file()
    failing_mock.read = Mock(side_effect=UnicodeDecodeError('', b'', 0, 0, ''))
    return failing_mock


@with_mock_file_factories({'utf': make_mock_file,
                           'iso': Mock(side_effect=[make_failing_mock(),
                                                    make_mock_file()])})


class TestEncodingHandling(unittest.TestCase):
    def test_read_code(self):
        _, encoding = read_code('utf')
        self.assertEqual(encoding, 'utf-8')
        _, encoding = read_code('iso')
        self.assertEqual(encoding, 'iso-8859-1')

if __name__ == '__main__':
    unittest.main()
