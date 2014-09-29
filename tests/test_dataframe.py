import json
import random
import pandas
from expr import Expr, NumExpr, DataFrameExpr

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
expr = Expr('*',
    [
        Expr('-',
            [
                DataFrameExpr(dataframe0),
                Expr('+',
                    [
                        NumExpr(32),
                        DataFrameExpr(dataframe1),
                    ]
                )
            ]
        ),
        Expr(operation_name='/',
                   arguments=[NumExpr(number=22),
                              NumExpr(number=7)])
    ]
)
resolved = expr.resolve()

def test_dataframe_numeric():
    print('')
    print(expr.resolve())
    expr.graph().write_png('expr.png')
    expr.serialise(json.dumps)
