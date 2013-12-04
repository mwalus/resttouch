#coding: utf-8

__version__ = '0.5.0'
__author__ = 'Marek Waluś <marekwalus@gmail.com>'


__all__ = ['Service', 'Route']

from resttouch.params import param_types
from resttouch.parsers import Parser
from requests import Request, Session
from urlparse import urljoin

AVAILABLE_METHODS = [
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'PATCH',
    'DELETE'
]


class Route(object):
    # Reference to service instance
    service = None
    name = ''

    def __init__(self, method, url, params, **kwargs):
        assert method in AVAILABLE_METHODS, \
            'Unrecognized method: %s' % method

        self.method = method
        self.url = url
        self.params = dict((param.value, param) for param in params)
        self.request_kwargs = kwargs

    def __call__(self, **kwargs):
        """
        Prepare data and start request
        """
        # Check if all keyword arguments are defined in route
        for name, value in kwargs.iteritems():
            if name not in self.params.keys():
                raise ValueError("Unknown parameter: %s, available parameters: " % name +
                                 ", ".join([p for p in self.params]))

        for name, param in self.params.iteritems():
            # Add default parameters to keyword arguments
            if name not in kwargs and param.default:
                kwargs[name] = param.default

            # If parameter is marked as required and not in keyword arguments
            elif name not in kwargs and param.required:
                raise ValueError('%s param is required!' % name)

        # group keyword argument by parameter base class
        groups = dict((p, {}) for p in param_types.keys())
        for name, value in kwargs.iteritems():
            for cls_name, cls in param_types.iteritems():
                if isinstance(self.params[name], cls):
                    groups[cls_name].update({name: value})

        # Create Session and Request instance
        session = Session()
        request = Request(
            method=self.method,
            url=urljoin(self.service.end_point, self.url % groups['PathParam']),
            params=groups['QueryParam'],
            data=groups['DataParam'],
            files=groups['FileParam'],
            **dict(self.service.globals, **self.request_kwargs)
        )
        # prepare_request
        prepped = session.prepare_request(request)

        # Trigger before_request
        if hasattr(self.service, 'before_request'):
            prepped = self.service.before_request(prepped)

        response = session.send(prepped)

        # Trigger after_request
        if hasattr(self.service, 'after_request'):
            response = self.service.after_request(response)

        # Trigger status code
        if hasattr(self.service, '%s_on_%s' % (self.name, response.status_code)):
            response = getattr(self.service, '%s_on_%s' % (self.name, response.status_code))(response)

        return response


class RouteMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['routes'] = [(route_name, obj) for route_name, obj in attrs.iteritems() if isinstance(obj, Route)]
        return super(RouteMetaclass, cls).__new__(cls, name, bases, attrs)


class Service(object):
    __metaclass__ = RouteMetaclass

    end_point = 'localhost'
    routes = []
    globals = {}
    output_parser = Parser

    def __init__(self):
        # Add service reference to all routes
        for name, route in self.routes:
            route.service = self
            route.name = name