"""preprocessor.py"""

import re


def hash_func(string, steps=0, number=2166136261):
    '''Generates a hash from a string.

    This function calculates the hash for a string, giving a result
    in the range [0,2**64[.
    '''
    in_bytes = bytes(string, encoding='utf-8')
    if steps == len(in_bytes):
        return number
    else:
        return hash_func(string,
                         steps+1,
                         (number*16777619) ^ (in_bytes[steps])) % (2**64)


def process(string):
    '''Processes a string, substituting suitable entries for their hashes.

    This function effectively processes strings, replacing _() macros
    containing strings with the same macro, but containing the string's
    hash.
    '''
    def hash_replace(match):
        '''
        This function takes a re.Match object as it's parameter and returns
        a string. The match object MUST be a match from the regexp used in
        process(). It is a match of something in the form _("str"), except
        for identifiers ending in _. The tests make this much clearer.
        '''
        return match.group(1) + "_(" + str(hash_func(match.group(2))) + ")"
    return re.sub('([^a-zA-Z0-9_]|^)_\("(.*?)"\)', hash_replace, string)
