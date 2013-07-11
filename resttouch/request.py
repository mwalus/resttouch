import urllib2
import urllib

__all__ = ('Request')


class Request(object):
    def __init__(self, url, data, body, headers={}):
        self.url = url
        self.data = data
        self.body = body
        self.headers = headers
        
    def get(self):
        request = urllib2.Request(
            url=self.url + '?' + urllib.urlencode(self.data),
            headers=self.headers
        )
        response = urllib2.urlopen(request)
        return response.read()
    
    def post(self):
        if self.body:
            data = self.body['body']
        else:
            data = urllib.urlencode(self.data)

        request = urllib2.Request(self.url, data, self.headers)
        response = urllib2.urlopen(request)
        return response.read()
    
    def put(self):
        pass
    
    def delete(self):
        pass