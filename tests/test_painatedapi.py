import unittest
import sys
import json

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock

from betterstack.uptime import PaginatedAPI
from betterstack.uptime.auth import BearerAuth


class PaginatedAPITests(unittest.TestCase):

    def mock_paginated_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code, ok):
                self.json_data = json_data
                self.status_code = status_code
                self.ok = ok

            def raise_for_status(self):
                if self.status_code != 200:
                    raise Exception

            def json(self):
                return self.json_data

        if kwargs['url'] == 'http://some.weird/api/v2/test_json' and not kwargs['params']:
            first_json = json.loads("""{
                "data": [
                    {
                        "hello": "World!"
                    }
                ],
                "pagination": {
                    "first": "https://betteruptime.com/api/v2/monitors?page=1",
                    "last": "https://betteruptime.com/api/v2/monitors?page=2",
                    "prev": null,
                    "next": "http://some.weird/api/v2/test_json?page=2"
                }
            }""")
            return MockResponse(first_json, 200, True)
        elif kwargs['url'] == 'http://some.weird/api/v2/test_json' and kwargs['params']['page'][0] == '2':
            second_json = json.loads("""{
                "data": [
                    {
                        "hello2": "World!"
                    }
                ],
                "pagination": {
                    "first": "https://betteruptime.com/api/v2/monitors?page=1",
                    "last": "https://betteruptime.com/api/v2/monitors?page=2",
                    "prev": null,
                    "next": null
                }
            }""")
            return MockResponse(second_json, 200, True)
        return MockResponse(None, 404, False)

    def setUp(self):
        self.api = PaginatedAPI(base_url="http://some.weird/api/v2/", auth=BearerAuth("HelloTest"))

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_paginated_get)
    def test_get(self, mock_get):
        resp = self.api.get("test_json")
        resp = [_ for _ in resp]
        self.assertEqual(2, len(resp))
