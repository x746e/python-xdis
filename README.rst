|buildstatus| |Supported Python Versions|

xdis
==========

Cross-Python bytecode Disassembler and Marshal routines


Introduction
------------

The Python `dis` module allows you to disassemble bytecode from the same
version of Python that you are running on. But what about bytecode from
different versions?

That's what this package is for. It can "marshal load" Python bytecodes
from different versions of Python. The command-line routine
*pydisasm* will show disassembly output using Python 3.5 disassembly conventions.

It accepts bytecodes from Python version 1.5 to 3.6 or so. The code
requires Python 2.6 or later and has been tested on Python running
versions 2.6, pypy-2.6.1 2.7, pypy-5.0.1, pypy-5.3.1, 3.2, 3.3, 3.4, 3.5
and 3.6.


Installation
------------

This uses setup.py, so it follows the standard Python routine:

::

    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    python setup.py install # may need sudo
    # or if you have pyenv:
    python setup.py develop

A GNU makefile is also provided so :code:`make install` (possibly as root or
sudo) will do the steps above.

Testing
-------

::

   make check

A GNU makefile has been added to smooth over setting running the right
command, and running tests from fastest to slowest.

If you have remake_ installed, you can see the list of all tasks
including tests via :code:`remake --tasks`.


Usage
-----

Run

::

     ./bin/pydisasm -h

for usage help.


As a drop-in replacement for dis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xdis also provides a drop in replacement for the standard dis module, this is useful if you
want to use the improved api from python 3.4 in python 2. For example:

>>> # works in python 2 and 3
>>> import xdis.std as dis
>>> [x.opname for x in dis.Bytecode('a = 10')]
['LOAD_CONST', 'STORE_NAME', 'LOAD_CONST', 'RETURN_VALUE']

See Also
--------

* https://github.com/rocky/python-uncompyle6 : python bytecode deparsing

.. |downloads| image:: https://img.shields.io/pypi/dd/xdis.svg
.. _trepan: https://pypi.python.org/pypi/trepan
.. _debuggers: https://pypi.python.org/pypi/trepan3k
.. _remake: http://bashdb.sf.net/remake
.. |buildstatus| image:: https://travis-ci.org/rocky/python-xdis.svg
		 :target: https://travis-ci.org/rocky/python-xdis
.. |Supported Python Versions| image:: https://img.shields.io/pypi/pyversions/xdis.svg
