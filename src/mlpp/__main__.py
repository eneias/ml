#!/usr/bin/env python3

'''ml_preprocessor: New Audaces ML reprocessor for C++ multilanguage code.

Usage:
    ml_preprocessor <C++ file>

This preprocesses C++ source code, replacing statements of form:

    _("String.")

By statements of the form:

    _(STR_HASH)

Where STR_HASH is the hash of the original string.

This can be replaced by a constexpr in C++11, whenever a compliant
compiler is available.
'''

import re
import sys

from ml import read_code, process


def main():
    '''Main function for the preprocessor.'''
    if len(sys.argv) != 2:
        print(re.sub('ml_preprocessor', sys.argv[0], __doc__))
        sys.exit(-1)

    code, input_encoding = read_code(sys.argv[1])

    sys.stdout = open(1, 'w', encoding=input_encoding, newline='\n',
                      closefd=False)

    print(process(code))

if __name__ == '__main__':
    main()
