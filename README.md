ml
==

This library contains functions for handling translations and source code
using the new Audaces ML translation system.

How to use
----------

Install through `pip`:

```bash
$ pip install -e git+https://github.com/Audaces/ml#egg=ml
```

How to develop
--------------

Make sure you have Python 3.4+ and `virtualenv`:

```bash
$ pip install virtualenv
```

Create a virtualenv and activate it:

```bash
$ virtualenv mlenv
```

And activate it:

```bash
$ . mlenv/Scripts/activate
```

Or on `cmd`

```bat
> mlenv\Scripts\activate
```

Install the required packages for development:

```bash
$ pip install -r test_dependencies.txt -r doc_dependencies.txt
```

Running tests
-------------

Run tests through `nose`:

```bash
$ nosetests
```

Run with `coverage`:

```bash
$ nosetests --with-coverage --cover-erase --cover-package src
```

Making executables for Windows
==============================

You will need cx-freeze. cx-freeze from pip is broken in Windows for
Python 3.4. You can get it from
http://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze.

Run:

```bash
$ python build.py build
```
