from resttouch import Service, parser, end_point
from resttouch.params import QueryParam
from resttouch.routes import Route
from resttouch.parser import JSONParser


@parser(JSONParser)
@end_point('https://ajax.googleapis.com/')
class GoogleService(Service):
    search = Route('GET', 'ajax/services/search/web', [
        QueryParam('v', default='1.1'),
        QueryParam('q')
    ], allow_redirects=True)

    def before_request(self, request):
        if request.params['q'] == 'python':
            print 'Searching for python!'
        return request

    def after_request(self, request, response):
        if request.params['v'] == '1.1' and response.status == 200:
            print 'Oh, version 1.1 is working!'
        return response

    def search_on_302(self, request, response):
        if request.params['q'] == 'move':
            print "We moved"
        return response

    def search_on_404(self, request, response):
        if request.params['q'] == 'python':
            print "Python not found?!"
        return response

if __name__ == "__main__":
    google = GoogleService()

    print google.search(q='python')
