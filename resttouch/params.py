from resttouch.serializators import PlainText

__all__ = ('PathParam', 'QueryParam', 'BodyContent')


class Param(object):
    required = True
    
    def __init__(self, value, default=None):
        self.value = str(value)
        self.default = default


class PathParam(Param):
    pass


class QueryParam(Param):
    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', True)
        super(QueryParam, self).__init__(*args, **kwargs)


class BodyContent(Param):
    def __init__(self, serializator=PlainText):
        self.serializator = serializator
        super(BodyContent, self).__init__(value='body', default=None)