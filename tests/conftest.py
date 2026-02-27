"""Pytest fixtures for API testing."""

import pytest

from betterstack.uptime import RESTAPI, BearerAuth, PaginatedAPI, UptimeAPI

from .fixtures import TEST_BASE_URL


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
