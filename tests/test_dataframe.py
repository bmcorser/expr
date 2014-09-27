import json
import random
import pandas
from expr_graph import Expression, NumericExpression, DataFrameExpression

dataframe_flat = lambda: (
    # index
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    # data
    [(random.randint(1, 10), random.randint(1, 10)) for _ in range(10)],
    # columns
    ('a', 'b'),
)
index, data, columns = dataframe_flat()
dataframe0 = pandas.DataFrame.from_records(index=index, data=data, columns=columns)
index, data, columns = dataframe_flat()
dataframe1 = pandas.DataFrame.from_records(index=index, data=data, columns=columns)
expr = Expression('*',
    [
        Expression('-',
            [
                DataFrameExpression(dataframe0),
                Expression('+',
                    [
                        NumericExpression(32),
                        DataFrameExpression(dataframe1),
                    ]
                )
            ]
        ),
        Expression(operation_name='/',
                   arguments=[NumericExpression(number=22),
                              NumericExpression(number=7)])
    ]
)
resolved = expr.resolve()

def test_dataframe_numeric():
    print('')
    print(expr.resolve())
    expr.serialise(json.dumps)
