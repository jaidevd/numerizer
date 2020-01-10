|Build Status|

numerizer
=========

A Python module to convert natural language numerics into ints and floats.
This is a port of the Ruby gem `numerizer
<https://github.com/jduff/numerizer.git>`_

Installation
------------

The NLG library can be installed from PyPI as follows:

.. code:: bash

    $ pip install numerizer

or from source as follows:

.. code:: bash

    $ git clone https://github.com/jaidevd/numerizer.git
    $ cd numerizer
    $ pip install -e .

Usage
-----

.. code:: python

    >>> from numerizer import numerize
    >>> numerize('forty two')
    '42'
    >>> numerize('forty-two')
    '42'
    >>> numerize('four hundred and sixty two')
    '462'
    >>> numerize('one fifty')
    '150'
    >>> numerize('twelve hundred')
    '1200'
    >>> numerize('twenty one thousand four hundred and seventy three')
    '21473'
    >>> numerize('one million two hundred and fifty thousand and seven')
    '1250007'
    >>> numerize('one billion and one')
    '1000000001'
    >>> numerize('nine and three quarters')
    '9.75'
    >>> numerize('platform nine and three quarters')
    'platform 9.75'


Extras
------

For R users, a wrapper library has been developed by `@amrrs <https://github.com/amrrs>`_. Try it out `here <https://github.com/amrrs/numerizer.git>`_.

.. |Build Status| image:: https://travis-ci.com/jaidevd/numerizer.svg?branch=master
   :target: https://travis-ci.com/jaidevd/numerizer
