from expr_graph import Expression, NumericExpression

arguments = (NumericExpression(3), NumericExpression(2))
operation_expected = (('*', 6),
                      ('+', 5),
                      ('/', 1.5),
                      ('-', 1),
                      ('%', 1))


def test_operations():
    for operation, expected in operation_expected:
        assert Expression(operation, arguments).resolve() == expected
