from resttouch.utils import RestTouchException
from example import TwitterService
import unittest

class TestRouteFunctions(unittest.TestCase):
    
    def setUp(self):
        self.service = TwitterService()

    def test_unknow_param(self):
        with self.assertRaises(RestTouchException): 
            self.service.retweeted_by(id=12345, bad_param=10)

    def test_no_required_param(self):
        with self.assertRaises(RestTouchException): 
            self.service.retweeted_by(count=20)
            
    def test_extra_query(self):
        self.assertRaises(self.service.users_shows(id=12345, extra_query={'include_entities': 'false'}), dict)
            
    def test_json_serializator_request(self):
        self.assertIsInstance(self.service.users_shows(id='6253282'), dict)
        

if __name__ == '__main__':
    unittest.main()