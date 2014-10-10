'''
Test for the .po exporter for .tra files.
'''

import unittest

from textwrap import dedent
from .__main__ import to_po


class TestPoExporter(unittest.TestCase):
    '''
    Test class for the po exporter.
    '''
    def test_to_po(self):
        t = ('Original', 'Translated')
        expected = dedent('''\
            msgid "Original"
            msgstr "Translated"''')
        self.assertEqual(to_po(t), expected)
