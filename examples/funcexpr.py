import pandas
from expr import (
    Expr as E,
    NumExpr as N,
    DataFrameExpr as D,
    FuncExpr as F,
)


def x_by_y(x, y, columns=False):
    data = [[a + b for b in range(x)] for a in range(y)]
    if columns is False:
        columns = [chr(97 + c) for c in range(x)]
    return pandas.DataFrame.from_records(data=data, columns=columns)


df_A = x_by_y(3, 4)
df_B = x_by_y(3, 4)
df_C = x_by_y(3, 4)

# import ipdb;ipdb.set_trace()
expr = E('+',
    [
        E('*',
            [
                N(3),
                F('pandas.concat',
                    [
                        D(x_by_y(1, 4, ['a'])),
                        D(x_by_y(1, 4, ['b'])),
                        D(x_by_y(1, 4, ['c'])),
                    ], axis=1
                )
            ]
        ),
        D(x_by_y(3, 4))
    ]
)
print(expr.resolve())
G = expr.graph()
G.write_png('func.png')
