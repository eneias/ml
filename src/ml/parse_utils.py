'''Utilities for parsing .tra files.

This is the module with parsing utilities for parsing files that are
a sequence of lines in the following form:

"Original string." = "Translated string."
'''

import re


def tuplify(string):
    '''Generates a tuple from a .tra file entry.

    This function takes a string of form '"original" = "translated"'
    and returns a tuple ("original", "translated"), or None if the
    string was malformed.
    '''
    reg = re.compile(r'"((?:\\"|.)*?)"\s*=\s*"((?:\\"|.)*?)"')
    result = reg.match(string)
    if result is None:
        return None
    else:
        return result.groups()


def errors(results):
    '''Pinpoints errors in the reading of a .tra file.

    This function gets a list of results (presumably from tuplify())
    and pairs it with numbers from 1 to len(l). It then filters it
    to get only the numbers where the list contained None, therefore
    filtering syntax errors.
    '''
    error_list = enumerate(results, 1)
    return [a for (a, b) in error_list if b is None]


def unnamespace(string, mark=''):
    '''Removes namespacing from a string.

    This is a helper function that takes a string of format
    "(<namespace>|)*<string>" and returns just the last one, adding marks to
    both sides as needed.
    '''
    return mark + string.split('|')[-1] + mark
