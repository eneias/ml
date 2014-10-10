import unittest
import random

from textwrap import dedent
from mock_utils.mock_file import with_mock_files
from .__main__ import (strip_uninteresting, make_tuples, parse_file,
                       concatenate_strings)

FILES = {'complete': dedent('''\
         msgid "Teste"
         msgstr "Test"
         msgid "Tradução"
         msgstr "Translation"
         '''),
         'untranslated': dedent('''\
         msgid "Teste"
         msgstr "Test"
         msgid "Tradução"
         msgstr ""
         '''),
         'multiline': dedent('''\
         msgid ""
         msgstr "Fake .po file header."
         msgid ""
         "This is a really\\n"
         "big sentence that\\n"
         "has been broken into\\n"
         "lines."
         msgstr ""
         "Esta é uma frase\\n"
         "realmente grande\\n"
         "que foi quebrada em\\n"
         "linhas."
         msgid "This is another quite\\nbig sentence\\nthat was only\\nbroken on translation."
         msgstr ""
         "Esta é outra frase\\n"
         "grande que foi somente\\n"
         "quebrada na tradução."
         msgid ""
         "Now this last sentence\\n"
         "was broken only on the\\n"
         "identifier."
         msgstr "Já esta última frase\\nfoi quebrada somente\\nno identificador."
         msgid "This string contains an escaped quote \\"."
         msgstr "Esta string contém aspas escapadas \\"."
         ''')}


@with_mock_files(FILES)
class TestPoImporter(unittest.TestCase):
    def test_strip_uninteresting(self):
        interesting_msgid = 'msgid "stuff"'
        interesting_msgstr = 'msgstr "other stuff"'
        uninteresting = '#, fuzzy'

        not_really_a_file = (([uninteresting] * 10) +
                             ([interesting_msgid] * random.randint(0, 10)) +
                             ([interesting_msgstr] * random.randint(0, 10)))
        random.shuffle(not_really_a_file)

        stripped = strip_uninteresting(not_really_a_file)

        self.assertEqual(stripped, list(filter(lambda x: x == interesting_msgid
                                               or x == interesting_msgstr,
                                               not_really_a_file)))

    def test_concatenate_strings(self):
        input = ('"This is a big" "" " string with\\nstuff"'
                 '" and more stuff.  "')
        expected = 'This is a big string with\\nstuff and more stuff.  '

        self.assertEqual(concatenate_strings(input), expected)

    def test_make_tuples(self):
        expected = [('Teste', 'Test'),
                    ('Tradução', 'Translation')]
        lines = list(open('complete', 'r'))
        self.assertEqual(make_tuples(lines), expected)

    def test_parse_file_complete(self):
        expected = [('Teste', 'Test'),
                    ('Tradução', 'Translation')]
        result = list(parse_file(open('complete', 'r')))
        self.assertEqual(result, expected)

    def test_parse_file_with_untranslated_messages(self):
        expected = [('Teste', 'Test'),
                    ('Tradução', '')]
        result = list(parse_file(open('untranslated', 'r')))
        self.assertEqual(result, expected)

    def test_parse_file_multiline(self):
        expected = [(r'This is a really\nbig sentence that\n'
                     r'has been broken into\nlines.',
                     r'Esta é uma frase\nrealmente grande\n'
                     r'que foi quebrada em\nlinhas.'),
                    (r'This is another quite\nbig sentence\n'
                     r'that was only\nbroken on translation.',
                     r'Esta é outra frase\ngrande que foi somente\n'
                     r'quebrada na tradução.'),
                    (r'Now this last sentence\nwas broken only on the\n'
                     r'identifier.',
                     r'Já esta última frase\nfoi quebrada somente\n'
                     r'no identificador.'),
                    (r'This string contains an escaped quote \".',
                     r'Esta string contém aspas escapadas \".')]
        result = list(parse_file(open('multiline', 'r')))
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
