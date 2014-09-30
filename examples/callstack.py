import pandas
from expr import (
    Expr as E,
    NumExpr as N,
    FuncExpr as F,
)

years = (1970, 1971, 1972, 1973, 1975, 1976, 1978, 1980, 1981, 1983, 1986, 1987, 1992, 2013)
F('sum', map(N, years)).graph().write_png('sabbathsum.png')
