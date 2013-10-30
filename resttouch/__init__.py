#coding: utf-8

__version__ = '0.5.0'
__author__ = 'Marek Waluś <marekwalus@gmail.com>'


__all__ = ['Service', 'Route']

from params import param_types

AVAILABLE_METHODS = [
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'PATCH',
    'DELETE'
]


def build_routes(bases, attrs):
    return [(route_name, obj) for route_name, obj in attrs.iteritems() if isinstance(obj, Route)]


class DeclarativeRouteMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['routes'] = build_routes(bases, attrs)
        new_class = super(DeclarativeRouteMetaclass,
                     cls).__new__(cls, name, bases, attrs)
        return new_class


class Service(object):
    __metaclass__ = DeclarativeRouteMetaclass
    
    end_point = 'localhost'
    headers = {}
    routes = []
    output_parser = None

    def __init__(self):
        for route_name, obj in self.routes:
            obj.service = self


class Route(object):
    service = None

    def __init__(self, method, url, params, **kwargs):
        assert method in AVAILABLE_METHODS, \
            'Unrecognized method: %s' % method

        self.method = method
        self.url = url
        self.params = dict((param.value, param) for param in params)
        self.kwargs = kwargs

    @property
    def grouped_params(self):
        groups = dict((klass, []) for name, klass in param_types)
        for name, param in self.params.iteritems():
            for param_type in groups.keys():
                if isinstance(param, param_type):
                    groups[param_type].append(param)
        return groups

    def __call__(self, **kwargs):
        # Check if all input parameters are defined in route
        for name, value in kwargs.iteritems():
            if name not in self.params.keys():
                raise ValueError("Unknown parameter: %s, available parameters: " % name +
                                 ", ".join([p for p in self.params]))

        for name, param in self.params.iteritems():
            # Add default parameters defined in route but not found in input_parameters
            if name not in kwargs and param.default:
                kwargs[name] = param.default

            # If parameter marked as required is not found in input_parameters raise ValueError
            elif name not in kwargs and param.required:
                raise ValueError('%s param is required!' % name)