'''Utilities for reading and writing .tra files and C++ sources.

Module for handling of C++ source code and .tra files.
'''

from glob import glob
from os.path import basename

from ml.parse_utils import tuplify, errors


def read_code(path):
    '''Reads C++ code and describes the encoding used.

    This function reads in a file and tries to guess its encoding, returning
    the text read and the encoding used.
    '''
    input_encoding = 'utf-8'
    with open(path, encoding=input_encoding) as file_handler:
        try:
            code = file_handler.read()
        except UnicodeDecodeError:
            file_handler.close()
            input_encoding = 'iso-8859-1'
            file_handler = open(path, encoding=input_encoding)
            code = file_handler.read()

    return code, input_encoding


def tra_file(tuples):
    '''Creates a string for writing a .tra file.

    This functions takes a list of tuples and returns string containing a valid
    .tra file, in sorted order.
    '''
    return "\n".join('"{0}" = "{1}"'.format(original, translation)
                     for original, translation in sorted(tuples))


def read_list(file_handler):
    '''Reads a list of translation tuples from a .tra file.

    This function takes a file handler and returns a list of tuples
    according to parse_utils.tuplify().
    '''
    results = [tuplify(line) for line in file_handler if line]
    error_list = errors(results)

    if error_list:
        raise ValueError('Malformed file, syntax error in lines: ' +
                         ', '.join(str(e) for e in error_list))
    else:
        return results


def read_dict(file_handler):
    '''Reads a dictionary of translations from a .tra file.

    This function takes a file handler and returns a dictionary mapping
    original strings to translated strings.
    '''
    return dict(read_list(file_handler))


def read_list_with_fallback(file_handler, fallback):
    '''Reads a list of translations from a .tra file, falling back when needed.

    This function takes two files and reads the first one of them as a
    list of tuples according to tuplify, and falling back to definitions
    in the second one for any tuple that has an empty translation string.
    '''
    base = read_dict(fallback)
    language_mapping = read_list(file_handler)

    complete = [(k, v) if v else (k, base[k]) for k, v in language_mapping]

    return complete


def read_all(directory):
    '''Reads a directory of tranlations.

    This function takes a directory path and reads every .tra file inside,
    returning a dictionary mapping the filenames to the translation
    dictionary as read by read_dict.
    '''
    pathes = glob(directory + '/*.tra')
    files = ((f, basename(f)) for f in pathes)
    languages = {}
    for filename, name in files:
        with open(filename, encoding='utf-8', newline='\n') as file_handler:
            languages[name] = read_dict(file_handler)
    return languages
