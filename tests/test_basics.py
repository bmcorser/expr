import json
from exp_graph import expression_from_dict, Expression, NumericExpression


pi_100 = Expression(operation_name='*',
                    arguments=[Expression(operation_name='/',
                                          arguments=[NumericExpression(number=22),
                                                     NumericExpression(number=7)]),
                               NumericExpression(100)])

resolved = pi_100.resolve()
expected_resolved = 314.2857142857143
serialised = pi_100.serialise(json.dumps)
expected_serialised = (
    '{"__type__": "Expression", "operation_name": "*", "arguments": '
        '['
            '{'
                '"__type__": "Expression", '
                '"operation_name": "/", '
                '"arguments": '
                    '['
                        '{'
                            '"__type__": "NumericExpression", '
                            '"number": 22.0'
                        '}, '
                        '{'
                            '"__type__": "NumericExpression", '
                            '"number": 7.0'
                        '}'
                    ']'
            '}, '
            '{'
                '"__type__": "NumericExpression", '
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
