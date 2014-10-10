'''
Tests for the translation source file generator.
'''

import unittest
from textwrap import dedent

from mock_utils.mock_file import with_mock_files
from mlcppgen.__main__ import templatefy_file, HEADER, FOOTER

FILES = {'complete': dedent('''\
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

EXPECTEDS = {'complete': dedent('''\
             template <>
             EXPORT_DLL std::string _("Test string.")
             { return fromUTF8("String de teste."); }

             template <>
             EXPORT_DLL std::string _("Another test.")
             { return fromUTF8("Outro teste."); }

             template <>
             EXPORT_DLL std::string _("Yet another.")
             { return fromUTF8("Ainda outra."); }

             template <>
             EXPORT_DLL std::string _("Terrible \\"corner case\\".")
             { return fromUTF8("Terrível \\"caso obscuro\\"."); }'''),
             'italian': dedent('''\
             template <>
             EXPORT_DLL std::string _("Test string.")
             { return fromUTF8("String di prova."); }

             template <>
             EXPORT_DLL std::string _("Another test.")
             { return fromUTF8("Outro teste."); }

             template <>
             EXPORT_DLL std::string _("Yet another.")
             { return fromUTF8("Ancora un'altra."); }''')}


def expected(s):
    '''Returns the expected output for a given mock file.'''
    return HEADER + EXPECTEDS[s] + FOOTER


class Helper:
    '''Helper functions for test refactoring.'''
    @with_mock_files(FILES)
    def check_generation(self, filename, fallback):
        '''Helper function for checking code generation.
        Checks the generated translation for a file and its fallback against
        the expected output.
        '''
        with open(filename, 'r') as file_handler, open(fallback, 'r') as fallback_file:
            templatefied = templatefy_file(file_handler,
                                           fallback=fallback_file)
        self.assertEqual(templatefied, expected(filename))


class TestGentranslation(unittest.TestCase, Helper):
    '''Test class for the translation source file generator.'''
    def test_complete_translation(self):
        self.check_generation('complete', fallback='complete')

    def test_incomplete_translation(self):
        self.check_generation('italian', fallback='complete')

if __name__ == '__main__':
    unittest.main()
