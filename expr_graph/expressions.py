import sys

import pydot

from .exceptions import MalformedExpressionException
from .operations import OPERATIONS


def _colour(dict_):
    'Allows for the use of the British English spelling of colour.'
    americanise = lambda s: s.replace('colour', 'color')
    return {americanise(k): v for k, v in dict_.iteritems()}


def expression_from_dict(dict_):
    try:
        class_name = dict_['__type__']
    except KeyError:
        raise MalformedExpressionException('I need a `__type__` key to know '
                                           'which class to instantiate.')
    expression_class = getattr(sys.modules[__name__], class_name)
    return expression_class.from_dict(dict_)


class ExpressionBase(object):
    serialisable_attrs = ()

    def to_dict(self):
        attrs = dict()
        for attr in self.serialisable_attrs:
            attrs.update({attr: getattr(self, attr)})
        return attrs

    @classmethod
    def from_dict(cls, json_dict):
        attrs = dict()
        for attr in cls.serialisable_attrs:
            try:
                attrs.update({attr: json_dict[attr]})
            except KeyError:
                exc = MalformedExpressionException
                cls_ = cls.__class__.__name__
                raise exc('Class {} requires argument {}'.format(cls_, attr))
        return cls(**attrs)

    def serialise(self, serialiser):
        return serialiser(self.to_dict())

    def resolve(self, *args, **kwargs):
        raise NotImplementedError("Should have implemented `resolve` method")

    @property
    def node(self):
        return pydot.Node(self.node_name,
                          style='filled',
                          **_colour(self.node_opts))

    def graph(self, name=None, graph=None, parent=None):
        if not graph:
            graph = pydot.Dot(name, graph_type='digraph')
        graph.add_node(self.node)
        if parent:
            graph.add_edge(pydot.Edge(self.node, parent))
        return graph

    def node_name(self, *args, **kwargs):
        raise NotImplementedError("Should have implemented `node_name` property.")  # NOQA


class Expression(ExpressionBase):
    __type__ = 'Expression'
    serialisable_attrs = ('__type__', 'operation_name', 'arguments')
    node_opts = {
        'fontcolour': '#DDDDDD',  # Silver
        'fontsize': '17.0',
        'fontname': 'Helvetica',
        'fixedsize': 'true',
        'width': '0.4',
        'height': '0.4',
        'colour': '#FF4136'  # Red
    }

    def __init__(self, operation_name, arguments, **kwargs):
        self.operation_name = operation_name
        self.operation = OPERATIONS.get(operation_name, False)
        if not self.operation:
            raise MalformedExpressionException(
                "Unsupported operation {}".format(operation_name))
        self.arguments = arguments

    @property
    def node_name(self):
        return self.operation_name

    @classmethod
    def from_dict(cls, json_dict):
        try:
            params = {'operation_name': json_dict['operation_name']}
            deserialised_args = map(expression_from_dict,
                                    json_dict['arguments'])
            params['arguments'] = deserialised_args
            return cls(**params)
        except KeyError:
            raise MalformedExpressionException('Expression object requires '
                                               '`operation_name` and '
                                               '`arguments` please pass them')

    def resolve(self):
        resolved_arguments = [arg.resolve() for arg in self.arguments]
        return self.operation(*resolved_arguments)

    def graph(self, name=None, graph=None, parent=None):
        """
        Build a graph of this expression, return `pydot.Dot` object.
        Reference for colours is at http://clrs.cc/
        To render a PNG image of the graph returned, simply call the
        `.write_png` method with the filename you with to write to.

        Example:

        >>> two = NumericExpression(2)
        >>> expression = Expression(operation='+', arguments=[two, two])
        >>> graph = expression.graph('Two and two')
        >>> graph.write_png('two-and-two.png')
        True
        """
        if not graph:
            graph = pydot.Dot(label=name, graph_type='digraph')
        graph.add_node(self.node)
        if parent:
            graph.add_edge(pydot.Edge(self.node, parent))
        for arg in self.arguments:
            graph = arg.graph(name, graph, self.node)
        return graph

    def to_dict(self):
        args_as_dicts = map(lambda arg: arg.to_dict(), self.arguments)
        return {
            '__type__': self.__type__,
            'operation_name': self.operation_name,
            'arguments': args_as_dicts
        }


class NumericExpression(ExpressionBase):
    __type__ = 'NumericExpression'
    serialisable_attrs = ('__type__', 'number')
    node_opts = {'colour': '#7FDBFF'}  # Aqua

    def __init__(self, number, **kwargs):
        try:
            self.number = float(number)
        except ValueError:
            messg = 'NumericExpression must be instantiated with a `Number`.'
            raise MalformedExpressionException(messg)

    @property
    def node_name(self):
        return repr(self.number)

    def resolve(self):
        return self.number


__all__ = ('expression_from_dict', 'Expression', 'NumericExpression')
