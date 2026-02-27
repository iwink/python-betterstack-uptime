"""Tests for PaginatedAPI class."""

import unittest

import responses

from betterstack.uptime import BearerAuth, PaginatedAPI
from tests.fixtures import TEST_BASE_URL


class TestPaginatedAPI(unittest.TestCase):
    """Tests for PaginatedAPI pagination handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = PaginatedAPI(base_url=TEST_BASE_URL, auth=BearerAuth("test-token"))

    @responses.activate
    def test_get(self):
        """Test paginated GET request that spans multiple pages."""
        # First page response
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"hello": "World!"}],
                "pagination": {
                    "first": "https://betteruptime.com/api/v2/monitors?page=1",
                    "last": "https://betteruptime.com/api/v2/monitors?page=2",
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",
                },
            },
            status=200,
        )

        # Second page response
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"hello2": "World!"}],
                "pagination": {
                    "first": "https://betteruptime.com/api/v2/monitors?page=1",
                    "last": "https://betteruptime.com/api/v2/monitors?page=2",
                    "prev": None,
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        self.assertEqual(len(resp), 2)
        self.assertEqual(resp[0], {"hello": "World!"})
        self.assertEqual(resp[1], {"hello2": "World!"})
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_get_single_page(self):
        """Test paginated GET request with only one page."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"single": "item"}],
                "pagination": {
                    "first": None,
                    "last": None,
                    "prev": None,
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0], {"single": "item"})
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_empty_response(self):
        """Test paginated GET request with no data."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [],
                "pagination": {
                    "first": None,
                    "last": None,
                    "prev": None,
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        self.assertEqual(len(resp), 0)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_single_object(self):
        """Test paginated GET request that returns a single object (not a list)."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors/1",
            json={
                "data": {
                    "id": "1",
                    "type": "monitor",
                    "attributes": {"url": "https://example.com"},
                },
            },
            status=200,
        )

        resp = list(self.api.get("monitors/1"))

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]["id"], "1")
