#!/usr/bin/env python
'''{executable_name}: New Audaces ML translation generator.

Usage:
    {executable_name} [--preprocess] <file>

This expects a .tra file as an argument, which shall be a sequence of lines
in the following form:

"Original string." = "Translated string."

And generates a C++ template specialization for each string, printing the
result to stdout.
'''

import sys
from textwrap import dedent

from ml import read_list_with_fallback
from ml import process as really_process

sys.stdout = open(1, 'w', encoding='utf-8', newline='\n', closefd=False)

HEADER = dedent('''\
        #ifdef AUDACES_ML

        #include <string>

        #include "multilanguage.h"

        #if defined(_WIN32) || defined(__WIN32__) || defined(WIN32) || \
defined(__CYGWIN__)
        # define EXPORT_DLL __declspec(dllexport)
        #else
        # define EXPORT_DLL
        #endif

        ''')

FOOTER = dedent('''\


         #endif
         ''')


def templatefy(strings):
    '''Creates C++ template specialization from translations.

    This function takes an iterable with two strings (a list or a tuple)
    and returns the C++ template with the strings in place.
    '''
    original, translated = strings
    return dedent('''\
    template <>
    EXPORT_DLL std::string _("{0}")
    {{ return "{1}"; }}''').format(original, translated)


def templatefy_file(translation_file, fallback):
    '''Create the full C++ file from a translation file, using a fallback.

    This function takes two file handlers, loads the second, falling back to
    the first for empty translations, and returns a string containing a C++
    description of the translation as template specializations.
    '''
    tuples = read_list_with_fallback(translation_file, fallback=fallback)
    return HEADER + "{templates}".format(templates='\n\n'.join(templatefy(t)
                                         for t in tuples)) + FOOTER


def main():
    '''Main generator logic.

    Main function for the program. Opens the file specified as an argument
    and prints the C++ generated code, preprocessed or not, depending on
    an option.
    '''
    args = sys.argv[:]
    fallback = None

    # Argument parsing.
    if '--preprocess' in args:
        args.remove('--preprocess')
        process = really_process
    else:
        process = lambda x: x

    if '--fallback' in args:
        index = args.index('--fallback')
        fallback = args[index + 1]
        args.remove('--fallback')
        args.remove(fallback)

    if len(args) != 2:
        print(__doc__.format(executable_name=args[0]))
        sys.exit(-1)

    translation_file = args[1]

    if fallback is None:
        fallback = translation_file

    with open(translation_file, encoding='utf-8') as file_handler, open(fallback, encoding='utf-8') as fallback:
        try:
            print(process(templatefy_file(file_handler, fallback=fallback)))
        except ValueError as exception:
            print(str(exception))

if __name__ == '__main__':
    main()
