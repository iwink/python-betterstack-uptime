"""Tests for RESTAPI class."""

import unittest

import responses

from betterstack.uptime import RESTAPI, BearerAuth
from betterstack.uptime.exceptions import (
    APIError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from tests.fixtures import TEST_BASE_URL


class TestRESTAPI(unittest.TestCase):
    """Tests for RESTAPI basic HTTP operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = RESTAPI(base_url=TEST_BASE_URL, auth=BearerAuth("test-token"))

    def test_rest_base_url_exception(self):
        """Test that base_url must end with a slash."""
        with self.assertRaises(ValueError) as ctx:
            RESTAPI(base_url="helloworld", auth=BearerAuth("test123"))
        self.assertIn("base_url should end with a /", str(ctx.exception))

    @responses.activate
    def test_get(self):
        """Test basic GET request."""
        test_json = {"data": [{"hello": "World!"}]}

        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}test_json",
            json=test_json,
            status=200,
        )

        resp = self.api.get("test_json")

        self.assertEqual(resp, test_json)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f"{TEST_BASE_URL}test_json")

    @responses.activate
    def test_get_with_parameters(self):
        """Test GET request with query parameters."""
        test_json = {"data": [{"id": 1}]}

        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json=test_json,
            status=200,
        )

        resp = self.api.get("monitors", parameters={"status": "up", "from_": "2023-01-01"})

        self.assertEqual(resp, test_json)
        # Check that trailing underscore was removed from 'from_'
        self.assertIn("from=2023-01-01", responses.calls[0].request.url)
        self.assertNotIn("from_", responses.calls[0].request.url)

    @responses.activate
    def test_post(self):
        """Test POST request."""
        request_body = {"url": "https://example.com", "monitor_type": "status"}
        response_json = {"data": {"id": "1", "attributes": request_body}}

        responses.add(
            responses.POST,
            f"{TEST_BASE_URL}monitors",
            json=response_json,
            status=201,
        )

        resp = self.api.post("monitors", body=request_body)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json(), response_json)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_patch(self):
        """Test PATCH request."""
        request_body = {"paused": True}
        response_json = {"data": {"id": "1", "attributes": {"paused": True}}}

        responses.add(
            responses.PATCH,
            f"{TEST_BASE_URL}monitors/1",
            json=response_json,
            status=200,
        )

        resp = self.api.patch("monitors/1", body=request_body)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), response_json)

    @responses.activate
    def test_delete(self):
        """Test DELETE request."""
        responses.add(
            responses.DELETE,
            f"{TEST_BASE_URL}monitors/1",
            status=204,
        )

        resp = self.api.delete("monitors/1")

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(responses.calls), 1)


class TestRESTAPIErrorHandling(unittest.TestCase):
    """Tests for RESTAPI error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = RESTAPI(base_url=TEST_BASE_URL, auth=BearerAuth("test-token"))

    @responses.activate
    def test_401_raises_authentication_error(self):
        """Test that 401 response raises AuthenticationError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Invalid token"},
            status=401,
        )

        with self.assertRaises(AuthenticationError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Invalid token", str(ctx.exception))

    @responses.activate
    def test_403_raises_forbidden_error(self):
        """Test that 403 response raises ForbiddenError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Access denied"},
            status=403,
        )

        with self.assertRaises(ForbiddenError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 403)

    @responses.activate
    def test_404_raises_not_found_error(self):
        """Test that 404 response raises NotFoundError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors/999",
            json={"error": "Monitor not found"},
            status=404,
        )

        with self.assertRaises(NotFoundError) as ctx:
            self.api.get("monitors/999")

        self.assertEqual(ctx.exception.status_code, 404)

    @responses.activate
    def test_429_raises_rate_limit_error(self):
        """Test that 429 response raises RateLimitError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Rate limit exceeded"},
            status=429,
            headers={"Retry-After": "60"},
        )

        with self.assertRaises(RateLimitError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 429)
        self.assertEqual(ctx.exception.retry_after, 60)

    @responses.activate
    def test_429_without_retry_after(self):
        """Test 429 response without Retry-After header."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Rate limit exceeded"},
            status=429,
        )

        with self.assertRaises(RateLimitError) as ctx:
            self.api.get("monitors")

        self.assertIsNone(ctx.exception.retry_after)

    @responses.activate
    def test_500_raises_server_error(self):
        """Test that 5xx response raises ServerError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Internal server error"},
            status=500,
        )

        with self.assertRaises(ServerError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 500)

    @responses.activate
    def test_502_raises_server_error(self):
        """Test that 502 response raises ServerError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Bad gateway"},
            status=502,
        )

        with self.assertRaises(ServerError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 502)

    @responses.activate
    def test_other_error_raises_api_error(self):
        """Test that other error codes raise generic APIError."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Bad request"},
            status=400,
        )

        with self.assertRaises(APIError) as ctx:
            self.api.get("monitors")

        self.assertEqual(ctx.exception.status_code, 400)

    @responses.activate
    def test_error_without_json_body(self):
        """Test error handling when response has no JSON body."""
        responses.add(
            responses.GET,
            f"{TEST_BASE_URL}monitors",
            body="Not Found",
            status=404,
        )

        with self.assertRaises(NotFoundError):
            self.api.get("monitors")

    @responses.activate
    def test_post_error_handling(self):
        """Test error handling for POST requests."""
        responses.add(
            responses.POST,
            f"{TEST_BASE_URL}monitors",
            json={"error": "Validation failed"},
            status=422,
        )

        with self.assertRaises(APIError) as ctx:
            self.api.post("monitors", body={"invalid": "data"})

        self.assertEqual(ctx.exception.status_code, 422)

    @responses.activate
    def test_delete_error_handling(self):
        """Test error handling for DELETE requests."""
        responses.add(
            responses.DELETE,
            f"{TEST_BASE_URL}monitors/999",
            json={"error": "Not found"},
            status=404,
        )

        with self.assertRaises(NotFoundError):
            self.api.delete("monitors/999")
