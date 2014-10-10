from unittest.mock import patch, Mock


def make_mock_file(text=''):
    '''Factory function for mock files.

    Creates a Mock for use in place of a file. Supports
    reading, use as context manager and iteration.
    '''
    def next_line(mock_file):
        current = mock_file.current
        mock_file.current += 1
        if current >= len(mock_file.lines):
            raise StopIteration
        return mock_file.lines[current]

    mock_file = Mock()
    mock_file.lines = text.split('\n')
    mock_file.current = 0
    mock_file.__enter__ = Mock(return_value=mock_file)
    mock_file.__exit__ = Mock()
    mock_file.__iter__ = Mock(return_value=mock_file)
    mock_file.__next__ = next_line
    return mock_file


def make_mock_open(files):
    '''Mock open factory.

    Creates a mock for the builtin open() function based on a
    dict that maps filenames to contents.
    '''
    def open_mock_file(filename, mode='', encoding=''):
        return make_mock_file(files[filename])
    return open_mock_file


def with_mock_files(files):
    '''Patcher for the builtin open.

    Decorator for a scope that patches the builtin open() function
    with a function from make_mock_open.
    '''
    def inner(c):
        return patch('builtins.open', make_mock_open(files))(c)
    return inner


def with_existing_mock_files(files):
    '''Patcher for the builtin open, with already mocked files.

    Decorator for a scope that patches the builtin open() function
    with a function from make_mock_open.
    '''
    def open_existing_mock_file(filename, mode='', encoding=''):
        return files[filename]

    def inner(c):
        return patch('builtins.open', open_existing_mock_file)(c)
    return inner
