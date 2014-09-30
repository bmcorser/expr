'Tests for the __eq__ method on BaseExpr'
from expr import (
    Expr as E,
    NumExpr as N,
    FuncExpr as F,
)


def test_eq_numexpr():
    'Can compare NumExpr objects'
    assert N(1) == N(1) is True
    assert N(1) == N(2) is False


def test_eq_funcexpr():
    'Can compare FuncExpr objects'
    assert F('sum', [N(1)]) == F('sum', [N(1)]) is True
    assert F('sum', [N(1)]) == F('sum', [N(2)]) is False
    # pylint: disable=line-too-long
    assert F('sum', [E('+', [N(2), N(2)])]) == F('sum', [E('+', [N(2), N(2)])]) is True  # NOQA
    assert F('sum', [E('+', [N(2), N(1)])]) == F('sum', [E('+', [N(2), N(2)])]) is False  # NOQA


def test_eq_types():
    'Can compare *Expr objects of different types'
    assert N(1) == F('sum', [N(1), N(2)]) is False
