from resttouch import Service, Route
from resttouch.params import QueryParam
from resttouch.parsers import JSONParser


class GoogleService(Service):
    end_point = 'https://ajax.googleapis.com/'
    parser = JSONParser

    globals = dict(
        #allow_redirects=True,
        headers={'user-agent': 'Python RestTouch v0.5'}
    )

    search = Route('GET', 'ajax/services/search/web', [
        QueryParam('v', default='1.1'),
        QueryParam('q')
    ])

    def before_request(self, request):
        print 'Before request'
        return request

    def after_request(self, response):
        print 'After request!'
        return response

    def search_on_200(self, response):
        print "200!"
        return response

    def search_on_302(self, response):
        print "We moved"
        return response

    def search_on_404(self, response):
        print "Python not found?!"
        return response

if __name__ == "__main__":
    google = GoogleService()

    print google.search(q='python')
