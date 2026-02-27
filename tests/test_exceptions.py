"""Tests for custom exceptions."""

import unittest

from betterstack.uptime.exceptions import (
    APIError,
    AuthenticationError,
    BetterStackError,
    ConfigurationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestAPIError(unittest.TestCase):
    """Tests for APIError base class."""

    def test_str_representation(self):
        """Test string representation includes status code."""
        error = APIError("Something went wrong", 500, {"error": "details"})

        result = str(error)

        self.assertEqual(result, "[500] Something went wrong")

    def test_properties(self):
        """Test error properties are set correctly."""
        error = APIError("Test error", 400, {"key": "value"})

        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.response_body, {"key": "value"})


class TestAuthenticationError(unittest.TestCase):
    """Tests for AuthenticationError."""

    def test_default_message(self):
        """Test default error message."""
        error = AuthenticationError()

        self.assertEqual(str(error), "[401] Invalid or missing authentication token")
        self.assertEqual(error.status_code, 401)

    def test_custom_message(self):
        """Test custom error message."""
        error = AuthenticationError("Token expired")

        self.assertEqual(str(error), "[401] Token expired")


class TestForbiddenError(unittest.TestCase):
    """Tests for ForbiddenError."""

    def test_default_message(self):
        """Test default error message."""
        error = ForbiddenError()

        self.assertEqual(str(error), "[403] Access denied")
        self.assertEqual(error.status_code, 403)


class TestNotFoundError(unittest.TestCase):
    """Tests for NotFoundError."""

    def test_default_message(self):
        """Test default error message."""
        error = NotFoundError()

        self.assertEqual(str(error), "[404] Resource not found")
        self.assertEqual(error.status_code, 404)


class TestRateLimitError(unittest.TestCase):
    """Tests for RateLimitError."""

    def test_default_message(self):
        """Test default error message without retry_after."""
        error = RateLimitError()

        self.assertEqual(str(error), "[429] Rate limit exceeded")
        self.assertEqual(error.status_code, 429)
        self.assertIsNone(error.retry_after)

    def test_with_retry_after(self):
        """Test error message includes retry_after information."""
        error = RateLimitError("Rate limit exceeded", retry_after=30)

        self.assertEqual(str(error), "[429] Rate limit exceeded (retry after 30s)")
        self.assertEqual(error.retry_after, 30)

    def test_custom_message_with_retry_after(self):
        """Test custom message with retry_after."""
        error = RateLimitError("Too many requests", retry_after=60)

        self.assertEqual(str(error), "[429] Too many requests (retry after 60s)")
        self.assertEqual(error.retry_after, 60)


class TestServerError(unittest.TestCase):
    """Tests for ServerError."""

    def test_default_message(self):
        """Test default error message."""
        error = ServerError()

        self.assertEqual(str(error), "[500] Server error")
        self.assertEqual(error.status_code, 500)

    def test_custom_status_code(self):
        """Test custom status code (e.g., 502, 503)."""
        error = ServerError("Bad gateway", status_code=502)

        self.assertEqual(str(error), "[502] Bad gateway")
        self.assertEqual(error.status_code, 502)


class TestValidationError(unittest.TestCase):
    """Tests for ValidationError."""

    def test_message(self):
        """Test validation error message."""
        error = ValidationError("Invalid parameter")

        self.assertEqual(str(error), "Invalid parameter")
        self.assertIsInstance(error, BetterStackError)


class TestConfigurationError(unittest.TestCase):
    """Tests for ConfigurationError."""

    def test_message(self):
        """Test configuration error message."""
        error = ConfigurationError("Missing API key")

        self.assertEqual(str(error), "Missing API key")
        self.assertIsInstance(error, BetterStackError)


class TestBetterStackError(unittest.TestCase):
    """Tests for BetterStackError base class."""

    def test_inheritance(self):
        """Test that BetterStackError inherits from Exception."""
        error = BetterStackError("Base error")

        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Base error")
