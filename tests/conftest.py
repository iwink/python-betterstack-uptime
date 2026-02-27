"""Pytest fixtures for API testing."""

import pytest

from betterstack.uptime import BearerAuth, PaginatedAPI, RESTAPI, UptimeAPI

from .fixtures import TEST_BASE_URL  # noqa: F401 - re-export for tests


@pytest.fixture
def uptime_api() -> UptimeAPI:
    """Create a UptimeAPI instance for testing."""
    return UptimeAPI("test-token")


@pytest.fixture
def rest_api() -> RESTAPI:
    """Create a RESTAPI instance for testing."""
    return RESTAPI(base_url=TEST_BASE_URL, auth=BearerAuth("test-token"))


@pytest.fixture
def paginated_api() -> PaginatedAPI:
    """Create a PaginatedAPI instance for testing."""
    return PaginatedAPI(base_url=TEST_BASE_URL, auth=BearerAuth("test-token"))
