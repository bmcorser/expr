# coding: utf-8
import json
from expr import expression_from_dict, Expr, NumExpr


pi_100 = Expr(operation_name='*',
                    arguments=[Expr(operation_name='/',
                                          arguments=[NumExpr(number=22),
                                                     NumExpr(number=7)]),
                               NumExpr(100)])

resolved = pi_100.resolve()
expected_resolved = 314.2857142857143
serialised = pi_100.serialise(json.dumps)
expected_serialised = (
    '{"__type__": "Expr", "operation_name": "*", "arguments": '
        '['
            '{'
                '"__type__": "Expr", '
                '"operation_name": "/", '
                '"arguments": '
                    '['
                        '{'
                            '"__type__": "NumExpr", '
                            '"number": 22.0'
                        '}, '
                        '{'
                            '"__type__": "NumExpr", '
                            '"number": 7.0'
                        '}'
                    ']'
            '}, '
            '{'
                '"__type__": "NumExpr", '
                '"number": 100.0'
            '}'
        ']'
    '}'
)
json_dict = json.loads(serialised)
deserialised = expression_from_dict(json_dict)
reserialised = deserialised.serialise(json.dumps)


def test_resolve():
    assert resolved == expected_resolved


def test_serialise():
    assert serialised == expected_serialised


def test_deserialise():
    assert deserialised.resolve() == expected_resolved


def test_reserialise():
    assert reserialised == expected_serialised
