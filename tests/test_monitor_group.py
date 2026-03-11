"""Tests for MonitorGroup API object."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import MonitorGroup
from tests.fixtures import BASE_URL, MONITOR_1, MONITOR_2, make_paginated_response

# MonitorGroup fixture data
MONITOR_GROUP_1 = {
    "data": {
        "id": "1",
        "type": "monitor_group",
        "attributes": {
            "name": "Production Monitors",
            "sort_index": 0,
            "created_at": "2023-05-01T00:00:00.000Z",
            "updated_at": "2023-05-08T00:00:00.000Z",
            "paused": False,
        },
    }
}


class TestMonitorGroup(unittest.TestCase):
    """Tests for MonitorGroup class operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    def test_create_monitor_group_from_response(self):
        """Test creating a MonitorGroup from API response."""
        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])

        self.assertEqual(group.id, "1")
        self.assertEqual(group.name, "Production Monitors")
        self.assertEqual(group.sort_index, 0)
        self.assertFalse(group.paused)

    def test_generate_url(self):
        """Test URL generation for MonitorGroup."""
        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])

        self.assertEqual(group.generate_url(), "monitor-groups/1")

    def test_generate_global_url(self):
        """Test global URL generation for MonitorGroup."""
        self.assertEqual(MonitorGroup.generate_global_url(), "monitor-groups")

    @responses.activate
    def test_fetch_monitors(self):
        """Test fetching monitors belonging to a group."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitor-groups/1/monitors",
            json=make_paginated_response([MONITOR_1["data"], MONITOR_2["data"]]),
            status=200,
        )

        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])
        group.fetch_monitors()

        self.assertIsNotNone(group._monitors)
        self.assertEqual(len(group._monitors), 2)
        self.assertEqual(group._monitors[0].url, "https://example.com")
        self.assertEqual(group._monitors[1].url, "https://secondexample.com")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_monitors_property_lazy_loading(self):
        """Test that monitors property triggers lazy loading."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitor-groups/1/monitors",
            json=make_paginated_response([MONITOR_1["data"]]),
            status=200,
        )

        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])

        # Initially _monitors should be None
        self.assertIsNone(group._monitors)

        # Accessing property should trigger fetch
        monitors = group.monitors

        self.assertEqual(len(monitors), 1)
        self.assertEqual(monitors[0].url, "https://example.com")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_monitors_property_caching(self):
        """Test that monitors property returns cached data on subsequent calls."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitor-groups/1/monitors",
            json=make_paginated_response([MONITOR_1["data"]]),
            status=200,
        )

        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])

        # First access triggers fetch
        monitors_first = group.monitors
        # Second access should use cached data
        monitors_second = group.monitors

        self.assertEqual(monitors_first, monitors_second)
        # Should only make one API call
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_monitors_property_empty_list(self):
        """Test monitors property with no monitors in group."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitor-groups/1/monitors",
            json=make_paginated_response([]),
            status=200,
        )

        group = MonitorGroup._from_api_response(self.api, MONITOR_GROUP_1["data"])
        monitors = group.monitors

        self.assertEqual(monitors, [])
        self.assertEqual(len(responses.calls), 1)
