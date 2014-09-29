expr
==========

.. figure:: https://raw.githubusercontent.com/bmcorser/expr/master/expr.png
   :alt: expr

Create simple visualisations of mathematical operations on `small datasets`_
by rendering an `expression graph`_, show your friends or serialise it for later.

.. _`expression graph`: https://code.google.com/p/pydot/
.. _`small datasets`: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html

Contents
--------

- `Usage`_

    * `Starting out`_
    * `Less verbosity`_
    * `Getting pandas involved`_

- `Known issues`_
- `Also`_

Usage
~~~~~

Examples follow using the Python interactive shell

Starting out
^^^^^^^^^^^^

Import some things from the module

.. code:: python

    from expr import Expr, NumExpr

Construct an expression

.. code:: python

    expr = Expr(
        operation_name='+',
        arguments=[
            NumExpr(number=1),
            Expr(
                operation_name='/',
                arguments=[
                    NumExpr(number=2),
                    NumExpr(number=3),
                ]
            )
        ]
    )

Get an answer

.. code:: python

    >> expr.resolve()
    1.6666666666666665

Draw a graph

.. code:: python

    >> graph = expr.graph()
    >> graph.write_png('example.png')
    True

``example.png``

.. figure:: https://raw.githubusercontent.com/bmcorser/expr/master/example.png
   :alt: example


Less verbosity
^^^^^^^^^^^^^^

Import things using ``as`` to save your typing fingers by aliasing those
characters away

.. code:: python

    >>> from expr import Expr as E, NumExpr as N
    >>> expr = E('/', [N(22), N(7)])
    >>> expr.resolve()
    3.142857142857143
    >>> expr.graph().write_png('pi.png')
    True

``pi.png``

.. figure:: https://raw.githubusercontent.com/bmcorser/expr/master/pi.png
   :alt: pi


Getting pandas involved
^^^^^^^^^^^^^^^^^^^^^^^

We can create expressions that involve more than just numbers ...

.. code:: python

    >>> import pandas
    >>> from expr import (
    ...     Expr as E,
    ...     NumExpr as N,
    ...     DataFrameExpr as D,
    ... )

Create some stupid datasets

.. code:: python

    >>> def two_by_four():
    ...     data = [(n + 1, n + 1) for n in range(4)]
    ...     return pandas.DataFrame.from_records(data=data, columns=['a', 'b'])

    >>> df_A = two_by_four()
    >>> df_B = two_by_four()
    >>> df_A
       a  b
    0  1  1
    1  2  2
    2  3  3
    3  4  4

Create the expression object, the ``DataFrameExpr`` object (aliased here
as ``D``) takes an optional argument ``name`` which will be used as a label if
present, otherwise an automatically generated label will applied.

.. code:: python

    >>> expr = E('*', [N(3), E('+', [D(df_A, 'A'), D(df_B, 'B')])])
    >>> expr.graph().write_png('dataframe.png')
    True
    >>> expr.resolve()
        0   1
    0   6   6
    1  12  12
    2  18  18
    3  24  24

``dataframe.png``

.. figure:: https://raw.githubusercontent.com/bmcorser/expr/master/dataframe.png
   :alt: dataframe

Known Issues
~~~~~~~~~~~~

If you like YAML, you may encounter_ some issues_ serialising ``pandas``
objects, but JSON should be fine.

.. _encounter: http://pyyaml.org/ticket/254
.. _issues: http://pyyaml.org/ticket/192

Also
~~~~

Colours courtesy of clrs.cc_

.. _clrs.cc: http://clrs.cc
