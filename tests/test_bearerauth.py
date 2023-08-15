import unittest
import sys

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock  # noqa: F401

from betterstack.uptime.auth import BearerAuth


class BearerAuthTests(unittest.TestCase):

    def test_bearer_auth(self):
        class MockRequest():
            headers = {}

        b = BearerAuth("mytesttoken")
        self.assertEqual(b.token, "mytesttoken")
        testrequest = MockRequest()
        testrequest = b.__call__(testrequest)

        self.assertTrue("authorization" in testrequest.headers)
        self.assertEqual(
            testrequest.headers['authorization'],
            "Bearer mytesttoken"
        )
