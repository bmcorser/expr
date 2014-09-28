# expr-graph

![expr-graph](https://raw.githubusercontent.com/bmcorser/expr-graph/master/expr-graph.png)

Create simple visualisations of mathematical operations on [small
datasets](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)
by rendering an [expression graph](https://code.google.com/p/pydot/), show your
friends or serialise it for later.

## Contents

 - [Usage](#usage)
  - [Starting out](#starting-out)
  - [Less verbosity](#less-verbosity)
  - [Involving pandas](#involving-pandas)
 - [Known issues](#known-issues)
 - [Also](#also)

### Usage

Examples follow using the Python interactive shell

#### Starting out

Import some things from the module

```python
from expr_graph import Expression, NumericExpression
```

Construct an expression

```python
expr = Expression(
    operation_name='+',
    arguments=[
        NumericExpression(number=1),
        Expression(
            operation_name='/',
            arguments=[
                NumericExpression(number=2),
                NumericExpression(number=3),
            ]
        )
    ]
)
```

Get an answer

```python
>> expr.resolve()
1.6666666666666665
```

Draw a graph

```python
>> graph = expr.graph()
>> graph.write_png('example.png')
True
```

`example.png`

![example](https://raw.githubusercontent.com/bmcorser/expr-graph/master/example.png)

#### Less verbosity

Import things using `as` to save your typing fingers by aliasing those
characters away

```python
>>> from expr_graph import Expression as E, NumericExpression as N
>>> expr = E('/', [N(22), N(7)])
>>> expr.resolve()
3.142857142857143
>>> expr.graph().write_png('pi.png')
True
>>> expr.resolve()
```

`pi.png`

![pi](https://raw.githubusercontent.com/bmcorser/expr-graph/master/pi.png)

#### Involving [`pandas`](http://pandas.pydata.org/)

```python
>>> from expr_graph import (
...     Expression as E,
...     NumericExpression as N,
...     DataFrameExpression as D,
... )
```

Create some stupid datasets

```python
>>> def two_by_four():
...     data = [(n + 1, n + 1) for n in range(4)]
...     return pandas.DataFrame.from_records(data=data, columns=['a', 'b'])

>>> dataframe_A = two_by_four()
>>> dataframe_B = two_by_four()
>>> dataframe_A
   a  b
0  1  1
1  2  2
2  3  3
3  4  4
```

Create the expression object, the `DataFrameExpression` object (aliased here as
`D`) takes an optional argument `name` which will be used as a label if
present, otherwise an automatically generated label will applied.

```python
>>> expr = E('*', [N(3), E('+', [D(dataframe_A, 'dataframe A'),
...                              D(dataframe_B, 'dataframe B')])])
>>> expr.graph().write_png('dataframe.png')
True
>>> expr.resolve()
    0   1
0   6   6
1  12  12
2  18  18
3  24  24
```

`dataframe.png`

![dataframe](https://raw.githubusercontent.com/bmcorser/expr-graph/master/dataframe.png)



### Issues

If you like YAML, you may [encounter](http://pyyaml.org/ticket/254) some
[issues](http://pyyaml.org/ticket/192) serialising `pandas` objects.

### Also

Colours courtesy of [clrs.cc](http://clrs.cc)
