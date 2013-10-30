from collections import namedtuple

__all__ = ('Request')

ParamGroup = namedtuple('ParamGroup', 'query, path, body')


class Request(object):
    def __init__(self, url, headers, params):
        self.url = url
        self.headers = headers
        self.params = params

    def get(self):
        pass

    def options(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

