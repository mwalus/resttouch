from resttouch import Service, Route
from resttouch.params import QueryParam
from resttouch.parsers import JSONParser


class GoogleService(Service):
    end_point = 'https://ajax.googleapis.com/'
    parser = JSONParser

    globals = dict(
        allow_redirects=True
    )

    search = Route('GET', 'ajax/services/search/web', [
        QueryParam('v', default='1.1'),
        QueryParam('q')
    ])

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
