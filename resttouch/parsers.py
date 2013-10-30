class Parser(object):
    def parse_request(self, request):
        return request

    def after_request(self, response):
        return response


class JSONParser(Parser):
    pass