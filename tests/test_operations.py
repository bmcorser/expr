from expr import Expr, NumExpr

arguments = (NumExpr(3), NumExpr(2))
operation_expected = (('*', 6),
                      ('+', 5),
                      ('/', 1.5),
                      ('-', 1),
                      ('%', 1))


def test_operations():
    for operation, expected in operation_expected:
        assert Expr(operation, arguments).resolve() == expected
