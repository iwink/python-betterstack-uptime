import unittest

from betterstack.uptime import BearerAuth


class BearerAuthTests(unittest.TestCase):
    def test_bearer_auth(self):
        class MockRequest:
            def __init__(self):
                self.headers = {}

        b = BearerAuth("mytesttoken")
        self.assertEqual(b.token, "mytesttoken")
        testrequest = MockRequest()
        testrequest = b(testrequest)

        self.assertIn("Authorization", testrequest.headers)
        self.assertEqual(testrequest.headers["Authorization"], "Bearer mytesttoken")
