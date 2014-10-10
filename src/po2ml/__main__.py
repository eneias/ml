#!/usr/bin/env python3

'''{executable_name}: Importer for .po files to Audaces ML new translation format.

Usage:
    {executable_name}: [--mark <mark>] [<file>]

This program imports .po (gettext translation) files to Audaces ML .tra format.

If a custom mark is set through --mark, it wil be placed on both ends of the
identifier as the default translation string for untranslated strings in the
.po file.

If no file is passed as an argument, the program reads from stdin.

Output is written to stdout.
'''

import sys
import re

from ml import tra_file

sys.stdout = open(1, 'w', encoding='utf-8', newline='\n', closefd=False)


def strip_uninteresting(file_handler):
    '''Removes irrelevant lines, or features the importer can't handle.

    This function takes a (presumably text, we hope) file and returns
    a list of strings containing only the strings deemed 'interesting',
    that is, the strings that start with "msgid", "msgstr" or "msgstr[0]",
    in THE SAME ORDER as they were in the file (really important).
    '''
    return [line.strip() for line in file_handler if line.startswith("msgid ")
            or line.startswith("msgstr ")
            or line.startswith("msgstr[0] ")
            or line.startswith('"')]


def concatenate_strings(input):
    '''Concatenates every string in an input describing strings.

    This function takes as its input a string containing a sequence of
    strings, delimited by '"'.
    '''
    strings = re.findall(r'"((?:\\"|.)*?)"', input)
    return ''.join(strings)


def make_tuples(lines):
    '''Actual parsing of the po file.

    This function takes a list of lines in the format returned by
    strip_uninteresting (check its docstring if needed) and pairs them up in
    a (msgid, msgstr) manner. This creates an output similar to the one used
    in the ml module.

    The input to the function is assumed to be correct already, as in no
    unpaired or out of order items are given.
    '''
    joined = ' '.join(lines)
    pieces = re.split(r'\s*msg(?:id|str)\s*', joined.strip())
    strings = [concatenate_strings(string) for string in pieces if string]
    result = []
    while strings:
        msgid, msgstr, *strings = strings
        if msgid:
            result.append((msgid, msgstr))
    return result


def parse_file(file_handler):
    '''Combines removal of uninteresting lines and the actual parsing.

    This function merely applies any marks needed to the output of make_tuples
    applied in a given file. In case of need, check their docstrings for an
    in-depth view of what they do.
    '''
    return (make_tuples(strip_uninteresting(file_handler)))


def main():
    '''Main logic for the importer.

    Main function for this program. It parses arguments looking for the
    definition of a custom mark, and applies parse_file() to the given input
    (file or stdin).
    '''
    args = sys.argv[1:]

    if len(args) > 1:
        print(__doc__.format(executable_name=sys.argv[0]))
        sys.exit(-1)

    if args:
        filename = args[0]
    else:
        filename = 0

    try:
        with open(filename, encoding='utf-8') as file_handler:
            print(tra_file(parse_file(file_handler)))
    except FileNotFoundError:
        print(filename, 'is not a valid file.')

if __name__ == '__main__':
    main()
