"""Tests for HeartbeatGroup API object."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import HeartbeatGroup
from tests.fixtures import BASE_URL, make_paginated_response


# HeartbeatGroup fixture data
HEARTBEAT_GROUP_1 = {
    "data": {
        "id": "1",
        "type": "heartbeat_group",
        "attributes": {
            "name": "Production Heartbeats",
            "sort_index": 0,
            "created_at": "2023-05-01T00:00:00.000Z",
            "updated_at": "2023-05-08T00:00:00.000Z",
            "paused": False,
        },
    }
}

# Heartbeat fixture data (for testing fetch_heartbeats)
HEARTBEAT_1 = {
    "id": "101",
    "type": "heartbeat",
    "attributes": {
        "name": "Cron Job 1",
        "period": 60,
        "grace": 30,
        "call": False,
        "sms": False,
        "email": True,
        "push": True,
        "team_wait": None,
        "heartbeat_group_id": 1,
        "sort_index": 0,
        "paused": False,
        "status": "up",
        "url": "https://uptime.betterstack.com/api/v1/heartbeat/abc123",
        "created_at": "2023-05-01T00:00:00.000Z",
        "updated_at": "2023-05-08T00:00:00.000Z",
    },
}

HEARTBEAT_2 = {
    "id": "102",
    "type": "heartbeat",
    "attributes": {
        "name": "Cron Job 2",
        "period": 300,
        "grace": 60,
        "call": False,
        "sms": False,
        "email": True,
        "push": True,
        "team_wait": None,
        "heartbeat_group_id": 1,
        "sort_index": 1,
        "paused": False,
        "status": "up",
        "url": "https://uptime.betterstack.com/api/v1/heartbeat/def456",
        "created_at": "2023-05-01T00:00:00.000Z",
        "updated_at": "2023-05-08T00:00:00.000Z",
    },
}


class TestHeartbeatGroup(unittest.TestCase):
    """Tests for HeartbeatGroup class operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    def test_create_heartbeat_group_from_response(self):
        """Test creating a HeartbeatGroup from API response."""
        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])

        self.assertEqual(group.id, "1")
        self.assertEqual(group.name, "Production Heartbeats")
        self.assertEqual(group.sort_index, 0)
        self.assertFalse(group.paused)

    def test_generate_url(self):
        """Test URL generation for HeartbeatGroup."""
        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])

        self.assertEqual(group.generate_url(), "heartbeat-groups/1")

    def test_generate_global_url(self):
        """Test global URL generation for HeartbeatGroup."""
        self.assertEqual(HeartbeatGroup.generate_global_url(), "heartbeat-groups")

    @responses.activate
    def test_fetch_heartbeats(self):
        """Test fetching heartbeats belonging to a group."""
        responses.add(
            responses.GET,
            f"{BASE_URL}heartbeat-groups/1/heartbeats",
            json=make_paginated_response([HEARTBEAT_1, HEARTBEAT_2]),
            status=200,
        )

        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])
        group.fetch_heartbeats()

        self.assertIsNotNone(group._heartbeats)
        self.assertEqual(len(group._heartbeats), 2)
        self.assertEqual(group._heartbeats[0].name, "Cron Job 1")
        self.assertEqual(group._heartbeats[1].name, "Cron Job 2")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_heartbeats_property_lazy_loading(self):
        """Test that heartbeats property triggers lazy loading."""
        responses.add(
            responses.GET,
            f"{BASE_URL}heartbeat-groups/1/heartbeats",
            json=make_paginated_response([HEARTBEAT_1]),
            status=200,
        )

        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])

        # Initially _heartbeats should be None
        self.assertIsNone(group._heartbeats)

        # Accessing property should trigger fetch
        heartbeats = group.heartbeats

        self.assertEqual(len(heartbeats), 1)
        self.assertEqual(heartbeats[0].name, "Cron Job 1")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_heartbeats_property_caching(self):
        """Test that heartbeats property returns cached data on subsequent calls."""
        responses.add(
            responses.GET,
            f"{BASE_URL}heartbeat-groups/1/heartbeats",
            json=make_paginated_response([HEARTBEAT_1]),
            status=200,
        )

        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])

        # First access triggers fetch
        heartbeats_first = group.heartbeats
        # Second access should use cached data
        heartbeats_second = group.heartbeats

        self.assertEqual(heartbeats_first, heartbeats_second)
        # Should only make one API call
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_heartbeats_property_empty_list(self):
        """Test heartbeats property with no heartbeats in group."""
        responses.add(
            responses.GET,
            f"{BASE_URL}heartbeat-groups/1/heartbeats",
            json=make_paginated_response([]),
            status=200,
        )

        group = HeartbeatGroup._from_api_response(self.api, HEARTBEAT_GROUP_1["data"])
        heartbeats = group.heartbeats

        self.assertEqual(heartbeats, [])
        self.assertEqual(len(responses.calls), 1)
