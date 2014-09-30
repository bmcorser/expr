import __builtin__
import importlib
import sys

import pandas
import pydot
import fn

import exceptions as exc
import operations as op


def _colour(dict_):
    'Allows for the use of the British English spelling of colour.'
    americanise = lambda s: s.replace('colour', 'color')
    return {americanise(k): v for k, v in dict_.iteritems()}


def expression_from_dict(dict_):
    try:
        class_name = dict_['__type__']
    except KeyError:
        raise exc.Malformed('I need a `__type__` key to know which class '
                                'to instantiate.')
    expression_class = getattr(sys.modules[__name__], class_name)
    return expression_class.from_dict(dict_)


class ExprBase(object):
    serialisable_attrs = ()

    def __eq__(self, other):
        if not self.serialisable_attrs:
            msg = 'Cannot test equality without `serialisable_attrs` attribute'
            raise NotImplementedError(msg)
        shared_attr = lambda attr: getattr(self, attr) == getattr(other, attr)
        try:
            return all([shared_attr(attr) for attr in self.serialisable_attrs])
        except AttributeError:
            return False

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.serialisable_attrs}

    @classmethod
    def from_dict(cls, json_dict):
        attrs = dict()
        for attr in cls.serialisable_attrs:
            try:
                attrs.update({attr: json_dict[attr]})
            except KeyError:
                exc = Malformed
                cls_ = cls.__class__.__name__
                raise exc('Class {} requires argument {}'.format(cls_, attr))
        return cls(**attrs)

    def serialise(self, serialiser, **kwargs):
        return serialiser(self.to_dict(), **kwargs)

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


class Expr(ExprBase):
    __type__ = 'Expr'
    serialisable_attrs = ('__type__', 'operation_name', 'arguments')
    node_opts = {
        'fontcolour': '#FFFFFF',  # White
        'fontsize': '17.0',
        'fontname': 'Helvetica',
        'fixedsize': 'true',
        'width': '0.4',
        'height': '0.4',
        'colour': '#FF4136'  # Red
    }

    def __init__(self, operation_name, arguments, **kwargs):
        self.operation_name = operation_name
        self.operation = op.OPERATIONS.get(operation_name, False)
        if not self.operation:
            raise Malformed(
                "Unsupported operation {}".format(operation_name))
        self.arguments = arguments

    @property
    def node_name(self):
        return op.OP_ALIAS.get(self.operation_name, self.operation_name)

    @classmethod
    def from_dict(cls, dict_):
        try:
            params = {'operation_name': dict_['operation_name']}
            deserialised_args = map(expression_from_dict, dict_['arguments'])
            params['arguments'] = deserialised_args
            return cls(**params)
        except KeyError:
            fmt_str = "{0} requires `operation_name` and `arguments`"
            raise Malformed(fmt_str.format(cls.__name__))

    def resolve(self, **kwargs):
        resolved_arguments = [arg.resolve() for arg in self.arguments]
        return self.operation(*resolved_arguments, **kwargs)

    def graph(self, name=None, graph=None, parent=None):
        if not graph:
            graph = pydot.Dot(label=name, graph_type='digraph')
        graph.add_node(self.node)
        if parent:
            graph.add_edge(pydot.Edge(self.node, parent))
        for arg in self.arguments:
            graph = arg.graph(name, graph, self.node)
        return graph

    def to_dict(self):
        return {
            '__type__': self.__type__,
            'operation_name': self.operation_name,
            'arguments': map(lambda arg: arg.to_dict(), self.arguments),
        }


class NumExpr(ExprBase):
    __type__ = 'NumExpr'
    serialisable_attrs = ('__type__', 'number')
    node_opts = {'colour': '#7FDBFF'}  # Aqua

    def __init__(self, number, **kwargs):
        try:
            self.number = float(number)
        except ValueError:
            messg = 'NumExpr must be instantiated with a `Number`.'
            raise Malformed(messg)

    @property
    def node_name(self):
        n = self.number
        return repr(int(n) if int(n) == float(n) else float(n))

    def resolve(self):
        return self.number


class DataFrameExpr(ExprBase):
    __type__ = 'DataFrameExpr'
    serialisable_attrs = ('__type__', 'dataframe')
    node_opts = {'colour': '#FFDC00'}  # Yellow

    def __init__(self, dataframe, name='auto', **kwargs):
        if not isinstance(dataframe, (pandas.DataFrame, pandas.Series)):
            messg = 'DataFrameExpr must be instantiated with a `DataFrame`.'
            raise Malformed(messg)
        self.dataframe = dataframe
        self.name = name

    @property
    def node_name(self):
        if self.name is 'auto':
            name = "df@{0}".format(hex(id(self.dataframe)))
        else:
            name = self.name
        return "{0}\n{1}".format(name, self.dataframe.shape)

    def to_dict(self):
        return {
            '__type__': self.__type__,
            'dataframe': self.dataframe.to_dict(),
            'name': self.name,
        }

    @classmethod
    def from_dict(cls, dict_):
        try:
            dict_.update({
                'dataframe': pandas.DataFrame.from_dict(dict_['dataframe']),
            })
            return cls(**dict_)
        except KeyError:
            raise Malformed('DataFrameExpr object requires `dataframe` '
                                'key, please pass it.')

    def resolve(self):
        return self.dataframe


class FuncExpr(Expr):
    __type__ = 'FuncExpr'
    node_opts = {
        'colour': '#F012BE',  # Fuchsia
        'fontname': 'Courier',
        'fontsize': '10',
    }

    def __init__(self, operation_name, arguments, **kwargs):
        dots = operation_name.split('.')
        name, dotted_path = dots[0], dots[1:]
        if dotted_path:
            module = importlib.import_module(name)
            self.operation = reduce(getattr, dotted_path, module)
        else:
            self.operation = getattr(__builtin__, name)
        self.operation_name = operation_name
        self.base_name = name
        self.dotted_path = dotted_path
        self.arguments = arguments
        self.kwargs = kwargs

    @property
    def node_name(self):
        if len(self.dotted_path) > 1:
            return "{0}...{1}".format(self.base_name, self.dotted_path[-1])
        elif len(self.dotted_path) == 1:
            return self.operation_name
        return self.base_name

    def resolve(self):
        try:
            return super(FuncExpr, self).resolve(**self.kwargs)
        except TypeError:
            resolved_arguments = [arg.resolve() for arg in self.arguments]
            return self.operation(resolved_arguments, **self.kwargs)

    def _kwargs_node(self, graph, kwargs):
        kwargs_fmt = ["{0}={1}".format(k, v) for k, v in self.kwargs.items()]
        kwargs_node = pydot.Node('\n'.join(kwargs_fmt),
                                 style='filled',
                                 **_colour({
                                     "colour": "#01FF70",  # Lime
                                     "fontname": "Courier",
                                     "fontsize": 9,
                                     }))
        graph.add_node(kwargs_node)
        graph.add_edge(pydot.Edge(kwargs_node, self.node, style='dashed'))

    def graph(self, *args, **kwargs):
        graph = super(FuncExpr, self).graph(*args, **kwargs)
        if kwargs:
            self._kwargs_node(graph, kwargs)
        return graph


__all__ = (
    'expression_from_dict',
    'Expr',
    'NumExpr',
    'DataFrameExpr',
    'FuncExpr'
)
