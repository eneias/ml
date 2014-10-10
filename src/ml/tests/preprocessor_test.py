import unittest

from ml.preprocessor import process, hash_func


class TestPreprocessor(unittest.TestCase):
    def test_base_case(self):
        s = '_("Base case")'
        expected = '_(' + str(hash_func('Base case')) + ')'
        self.assertEqual(process(s), expected)

    def test_identifier_ends_in_underscore(self):
        s = 'cornerCase_("this should not match")'
        self.assertEqual(process(s), s)

    def test_not_a_c_string_inside_macro(self):
        s = '_(shouldNotMatch)'
        self.assertEqual(process(s), s)

    def test_2_macros_1_line(self):
        s = '_("Should") _("Match")'
        expected = ('_(' + str(hash_func('Should')) + ') _(' +
                    str(hash_func('Match')) + ')')
        self.assertEqual(process(s), expected)

    def test_2_macros_1_wrong(self):
        s = '_("Should") _(NotMatch)'
        expected = ('_(' + str(hash_func('Should')) + ') _(NotMatch)')
        self.assertEqual(process(s), expected)

    def test_expected_common_usage(self):
        s = 'normal usage _("Match")'
        expected = 'normal usage _(' + str(hash_func('Match')) + ')'
        self.assertEqual(process(s), expected)

if __name__ == '__main__':
    unittest.main()
