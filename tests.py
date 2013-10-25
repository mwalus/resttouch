from google import GoogleService
import unittest


class TestRouteFunctions(unittest.TestCase):
    def setUp(self):
        self.service = GoogleService()

    def test_unknown_param(self):
        with self.assertRaises(ValueError):
            self.service.search(id=12345, bad_param=10)

    def test_no_required_param(self):
        with self.assertRaises(ValueError):
            self.service.search()

    def test_json_parser_request(self):
        self.assertIsInstance(self.service.search(id='python'), dict)
        

if __name__ == '__main__':
    unittest.main()