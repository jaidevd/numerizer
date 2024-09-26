numerizer
=========

A Python module to convert natural language numerics into ints and floats.
This is a port of the Ruby gem `numerizer
<https://github.com/jduff/numerizer.git>`_

Numerizer has been tested on Python 3.9, 3.10 and 3.11.

Installation
------------

The numerizer library can be installed from PyPI as follows:

.. code:: bash

    $ pip install numerizer

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


Using the SpaCy extension
^^^^^^^^^^^^^^^^^^^^^^^^^

Since version 0.2, numerizer is available as a `SpaCy extension <https://spacy.io/usage/processing-pipelines#custom-components-attributes>`_.

Any named entities of a quantitative nature within a SpaCy document can be numerized as follows:

.. code:: python

    >>> from spacy import load
    >>> nlp = load('en_core_web_sm')  # or load any other spaCy model
    >>> doc = nlp('The projected revenue for the next quarter is over two million dollars.')
    >>> doc._.numerize()
    {the next quarter: 'the next 1/4', over two million dollars: 'over 2000000 dollars'}

Users can specify which entity types are to be numerized, by using the `labels` argument in the extension function, as follows:

.. code:: python

    >>> doc._.numerize(labels=['MONEY'])  # only numerize entities of type 'MONEY'
    {over two million dollars: 'over 2000000 dollars'}


The extension is available for tokens and spans as well.

.. code:: python

    >>> two_million = doc[-4:-2]  # span corresponding to "two million"
    >>> two_million._.numerize()
    '2000000'
    >>> quarter = doc[6]  # token corresponding to "quarter"
    >>> quarter._.numerized
    '1/4'


Extras
------

For R users, a wrapper library has been developed by `@amrrs <https://github.com/amrrs>`_. Try it out `here <https://github.com/amrrs/numerizer.git>`_.
