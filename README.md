RestTouch v0.5
=========
REST client for Python based on Requests (https://github.com/kennethreitz/requests)

## Installation:
    pip install resttouch

## Example usage:
        from resttouch import Service, Route
        from resttouch.params import QueryParam
        from resttouch.parsers import plain, json_parser


        class GoogleService(Service):
            end_point = 'https://ajax.googleapis.com/'
            input_data_parser = plain
            output_parser = json_parser

            request_globals = dict(
                headers={'user-agent': 'Python RestTouch v0.5'}
            )

            session_globals = dict(
                allow_redirects=True
            )

            search = Route('GET', 'ajax/services/search/web', [
                QueryParam('v', default='1.1'),
                QueryParam('q')
            ])

            def before_request(self, request):
                if request.body is None:
                    print 'No body needed for this request ;-)'
                return request

            def after_request(self, response):
                if 'javascript' in response.headers['content-type']:
                    print "Ladies and Gentlemen, we got JSON here!"
                return response

            def search_on_200(self, response):
                print 'Got 200 Status!'
                return response

            def search_on_404(self, response):
                print "Python not found?!"
                return response

        if __name__ == "__main__":
            google = GoogleService()

            print google.search(q='python')
