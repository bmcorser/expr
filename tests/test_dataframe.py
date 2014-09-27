import pandas
import yaml
from expr_graph import Expression, NumericExpression, DataFrameExpression

dataframe_flat = (
    # index
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    # data
    [
        (0, 9),
        (1, 8),
        (2, 7),
        (3, 6),
        (4, 5),
        (5, 4),
        (6, 3),
        (7, 2),
        (8, 1),
        (9, 0),
    ],
    # columns
    ('a', 'b'),
)
index, data, columns = dataframe_flat
dataframe0 = pandas.DataFrame.from_records(index=index, data=data, columns=columns)
dataframe1 = pandas.DataFrame.from_records(index=index, data=data, columns=columns)
expr = Expression('*',
    [
        Expression('+',
            [
                DataFrameExpression(dataframe0),
                DataFrameExpression(dataframe1)
            ]
        ),
        NumericExpression(3)
    ]
)
resolved = expr.resolve()

def test_dataframe_numeric():
    expr.serialise(yaml.dump)  # uh oh
