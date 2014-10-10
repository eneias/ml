#!/usr/bin/env python3

'''ml2po: Exporter for Audaces ML new translation format to .po files.

Usage:
    ml2po [<file>]

This program exports Audaces ML .tra files to .po (gettext translation) format.

The program will output a .po header (msgid "") informing the charset to be
used, (UTF-8, don't touch it!). If changed, gettext tools will malfunction,
because the output of this program is in UTF-8 anyway, unless you change
that too, which is a bad idea anyway.

If no file is passed as an argument, the program reads from stdin.

Output is written to stdout.
'''

import re
import sys

from ml import read_list
from textwrap import dedent

sys.stdout = open(1, 'w', encoding='utf-8', newline='\n', closefd=False)


def to_po(pair):
    '''Generate a po entry from a translation pair.

    Args:
        pair (tuple): an original-translation pair

    Return:
        str: the pair formatted as a msgid/msgstr gettext .po pair.
    '''
    return dedent('''\
            msgid "{0}"
            msgstr "{1}"'''.format(*pair))


def main():
    '''Export a ML .tra file to .po format.

    This is the main function for the program, it looks for an argument
    to open as the input file, or uses stdin, and maps to_po over a
    list returned by parse_utils.read_list when applied to the file.
    '''
    args = sys.argv[1:]

    if len(args) > 1:
        print(re.sub('ml2po', sys.argv[0], __doc__))
        sys.exit(-1)

    if args:
        filename = args[0]
    else:
        filename = 0

    try:
        with open(filename, encoding='utf-8') as file_handler:
            print('msgid ""\nmsgstr "Content-Type:'
                  ' text-plain; charset=UTF-8\\n"')
            for line in (to_po(line) for line in read_list(file_handler)):
                print(line)
    except FileNotFoundError:
        print(filename, 'is not a valid file.')

if __name__ == "__main__":
    main()
