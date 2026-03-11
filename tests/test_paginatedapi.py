"""Tests for PaginatedAPI class."""

import json
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

    @responses.activate
    def test_get_concurrent_multiple_pages(self):
        """Test concurrent fetching of multiple pages."""
        page_responses = {
            None: {
                "data": [{"id": "1", "name": "item1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=3",
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",
                },
            },
            "1": {
                "data": [{"id": "1", "name": "item1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=3",
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",
                },
            },
            "2": {
                "data": [{"id": "2", "name": "item2"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=3",
                    "prev": f"{TEST_BASE_URL}test_json?page=1",
                    "next": f"{TEST_BASE_URL}test_json?page=3",
                },
            },
            "3": {
                "data": [{"id": "3", "name": "item3"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=3",
                    "prev": f"{TEST_BASE_URL}test_json?page=2",
                    "next": None,
                },
            },
        }

        def page_callback(request):
            from urllib.parse import parse_qs, urlparse

            parsed = urlparse(request.url)
            params = parse_qs(parsed.query)
            page = params.get("page", [None])[0]
            body = page_responses.get(page, page_responses[None])
            return (200, {}, json.dumps(body))

        responses.add_callback(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            callback=page_callback,
            content_type="application/json",
        )

        resp = list(self.api.get("test_json"))

        # Should have all 3 items
        self.assertEqual(len(resp), 3)
        # Items should be in order (page 1, then pages 2 and 3 in order)
        self.assertEqual(resp[0]["id"], "1")
        self.assertEqual(resp[1]["id"], "2")
        self.assertEqual(resp[2]["id"], "3")
        # Should have made 3 requests total
        self.assertEqual(len(responses.calls), 3)

    @responses.activate
    def test_get_sequential_fallback_no_last_url(self):
        """Test sequential fallback when pagination has no last URL."""
        # First page response without 'last' URL - triggers sequential fallback
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": None,  # No last URL - can't determine total pages
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
                "data": [{"id": "2"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": None,
                    "prev": f"{TEST_BASE_URL}test_json?page=1",
                    "next": None,  # No more pages
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        self.assertEqual(len(resp), 2)
        self.assertEqual(resp[0]["id"], "1")
        self.assertEqual(resp[1]["id"], "2")
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_get_single_page_with_last_url(self):
        """Test single page response where last URL points to page 1."""
        # Response where total pages is 1 (early return path)
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=1",  # Only 1 page
                    "prev": None,
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]["id"], "1")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_invalid_page_in_last_url(self):
        """Test fallback when last URL has invalid page parameter."""
        # First page with invalid page number in last URL
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=invalid",  # Invalid page
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",
                },
            },
            status=200,
        )

        # Second page (sequential fallback)
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "2"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=2",
                    "prev": f"{TEST_BASE_URL}test_json?page=1",
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        # Should fall back to sequential and still get all items
        self.assertEqual(len(resp), 2)
        self.assertEqual(resp[0]["id"], "1")
        self.assertEqual(resp[1]["id"], "2")

    @responses.activate
    def test_get_last_url_missing_page_param(self):
        """Test fallback when last URL is present but has no page parameter."""
        # First page with last URL but no page query parameter
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json",
                    "last": f"{TEST_BASE_URL}test_json",  # No page param
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",
                },
            },
            status=200,
        )

        # Second page (sequential fallback)
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "2"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=2",
                    "prev": f"{TEST_BASE_URL}test_json?page=1",
                    "next": None,
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        # Should fall back to sequential and still get all items
        self.assertEqual(len(resp), 2)

    def test_max_workers_parameter(self):
        """Test that max_workers parameter is properly set."""
        api_default = PaginatedAPI(base_url=TEST_BASE_URL, auth=BearerAuth("token"))
        self.assertEqual(api_default.max_workers, 5)

        api_custom = PaginatedAPI(base_url=TEST_BASE_URL, auth=BearerAuth("token"), max_workers=10)
        self.assertEqual(api_custom.max_workers, 10)

    def test_get_total_pages_method(self):
        """Test _get_total_pages method directly."""
        # Valid pagination with page number
        pagination = {"last": "https://api.example.com/resources?page=5"}
        self.assertEqual(self.api._get_total_pages(pagination), 5)

        # No last URL
        pagination = {"last": None}
        self.assertIsNone(self.api._get_total_pages(pagination))

        # Empty pagination
        pagination = {}
        self.assertIsNone(self.api._get_total_pages(pagination))

        # Last URL without page parameter
        pagination = {"last": "https://api.example.com/resources"}
        self.assertIsNone(self.api._get_total_pages(pagination))

        # Invalid page value
        pagination = {"last": "https://api.example.com/resources?page=abc"}
        self.assertIsNone(self.api._get_total_pages(pagination))

    @responses.activate
    def test_get_inconsistent_pagination_single_page(self):
        """Test handling of inconsistent pagination (next exists but last=page 1)."""
        # Edge case: API returns next URL but last says page 1
        # This tests the `total_pages <= 1` early return (line 375)
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json={
                "data": [{"id": "1"}],
                "pagination": {
                    "first": f"{TEST_BASE_URL}test_json?page=1",
                    "last": f"{TEST_BASE_URL}test_json?page=1",  # Says only 1 page
                    "prev": None,
                    "next": f"{TEST_BASE_URL}test_json?page=2",  # But has next (inconsistent)
                },
            },
            status=200,
        )

        resp = list(self.api.get("test_json"))

        # Should only return first page data (trusts last URL over next)
        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]["id"], "1")
        # Only one request made - did not follow next
        self.assertEqual(len(responses.calls), 1)
