import unittest
import sys, json

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock

from betterstack.uptime import RESTAPI
from betterstack.uptime.auth import BearerAuth

class RESTAPITests(unittest.TestCase):

    def setUp(self):
        self.api = RESTAPI(base_url="http://some.weird/api/v2/", auth=BearerAuth("HelloTest"))

    def test_rest_base_url_exception(self):
        with self.assertRaises(ValueError) as c:
            api = RESTAPI(base_url="helloworld", auth=BearerAuth("test123"))
        self.assertTrue("base_url should end with a /" in str(c.exception))
    

    @mock.patch('betterstack.uptime.requests.get')
    def test_get(self, mock_get):
        test_json = json.loads("""{
                "data": [
                    {
                        "hello": "World!"
                    }
                ]
            }""")

        mock_get.return_value = mock.Mock(ok=True, status_code=200)
        mock_get.return_value.json.return_value = test_json

        
        resp = self.api.get("test_json")

        self.assertEqual(resp, test_json)


    