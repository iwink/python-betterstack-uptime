"""Tests for OnCallCalendar and OnCallEvent."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import OnCallCalendar, OnCallEvent

from .fixtures import BASE_URL, make_paginated_response


class TestOnCallCalendar(unittest.TestCase):
    """Tests for the OnCallCalendar class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.calendar_data = {
            "id": "12345",
            "type": "on_call_calendar",
            "attributes": {
                "name": None,
                "default_calendar": True,
                "team_name": "Production",
            },
            "relationships": {
                "on_call_users": {
                    "data": [
                        {
                            "id": "2345",
                            "type": "user",
                            "meta": {"email": "tomas@betterstack.com"},
                        }
                    ]
                }
            },
        }

    def test_create_calendar_from_response(self):
        """Test creating an OnCallCalendar from API response."""
        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)

        self.assertEqual(calendar.id, "12345")
        self.assertEqual(calendar.type, "on_call_calendar")
        self.assertIsNone(calendar.name)
        self.assertTrue(calendar.default_calendar)
        self.assertEqual(calendar.team_name, "Production")

    def test_on_call_users_property(self):
        """Test that on_call_users are correctly parsed from relationships."""
        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)

        users = calendar.on_call_users
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["id"], "2345")
        self.assertEqual(users[0]["type"], "user")

    def test_on_call_users_empty(self):
        """Test on_call_users when no relationships data."""
        data = {
            "id": "123",
            "type": "on_call_calendar",
            "attributes": {
                "name": "Empty Calendar",
                "default_calendar": False,
                "team_name": "Test",
            },
        }

        calendar = OnCallCalendar._from_api_response(self.api, data)

        self.assertEqual(calendar.on_call_users, [])

    def test_generate_url(self):
        """Test URL generation for OnCallCalendar."""
        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)
        self.assertEqual(calendar.generate_url(), "on-calls/12345")

    def test_generate_global_url(self):
        """Test global URL generation for OnCallCalendar."""
        self.assertEqual(OnCallCalendar.generate_global_url(), "on-calls")

    @responses.activate
    def test_get_all_calendars(self):
        """Test fetching all on-call calendars."""
        responses.add(
            responses.GET,
            f"{BASE_URL}on-calls",
            json=make_paginated_response([self.calendar_data]),
            status=200,
        )

        calendars = list(OnCallCalendar.get_all_instances(self.api))

        self.assertEqual(len(calendars), 1)
        self.assertEqual(calendars[0].team_name, "Production")
        self.assertTrue(calendars[0].default_calendar)

    @responses.activate
    def test_fetch_events(self):
        """Test fetching events for an on-call calendar."""
        event_data = {
            "id": "56789",
            "type": "on_call_event",
            "attributes": {
                "starts_at": "2025-01-01T09:00:00Z",
                "ends_at": "2025-01-01T17:00:00Z",
                "users": ["tomas@betterstack.com"],
                "override": False,
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}on-calls/12345/events",
            json=make_paginated_response([event_data]),
            status=200,
        )

        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)
        events = calendar.fetch_events()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].starts_at, "2025-01-01T09:00:00Z")
        self.assertEqual(events[0].users, ["tomas@betterstack.com"])

    @responses.activate
    def test_events_property_lazy_loading(self):
        """Test lazy loading of events via property."""
        event_data = {
            "id": "56789",
            "type": "on_call_event",
            "attributes": {
                "starts_at": "2025-01-01T09:00:00Z",
                "ends_at": "2025-01-01T17:00:00Z",
                "users": ["user@example.com"],
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}on-calls/12345/events",
            json=make_paginated_response([event_data]),
            status=200,
        )

        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)

        # First access triggers fetch
        events = calendar.events
        self.assertEqual(len(events), 1)

        # Second access uses cache
        _ = calendar.events
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_rotation(self):
        """Test creating a rotation for an on-call calendar."""
        rotation_response = {
            "rotation_length": 8,
            "rotation_interval": "hour",
            "start_rotations_at": "2025-02-01T07:00:00.000Z",
            "end_rotations_at": "2027-02-01T07:00:00.000Z",
            "users": ["bob@betterstack.com", "alice@betterstack.com"],
        }
        responses.add(
            responses.POST,
            f"{BASE_URL}on-calls/12345/rotation",
            json=rotation_response,
            status=200,
        )

        calendar = OnCallCalendar._from_api_response(self.api, self.calendar_data)
        result = calendar.create_rotation(
            users=["bob@betterstack.com", "alice@betterstack.com"],
            rotation_length=8,
            rotation_period="hour",
            start_rotations_at="2025-02-01T07:00:00Z",
            end_rotations_at="2027-02-01T07:00:00Z",
        )

        self.assertEqual(result["rotation_length"], 8)
        self.assertEqual(result["rotation_interval"], "hour")
        self.assertEqual(len(result["users"]), 2)

    def test_create_rotation_without_api_raises(self):
        """Test that create_rotation raises without API."""
        calendar_data = {
            "id": "123",
            "type": "on_call_calendar",
            "attributes": {
                "name": "Test",
                "default_calendar": False,
                "team_name": "Test",
            },
        }
        calendar = OnCallCalendar._from_api_response(None, calendar_data)

        with self.assertRaises(ValueError) as context:
            calendar.create_rotation(
                users=["user@example.com"],
                rotation_length=1,
                rotation_period="day",
                start_rotations_at="2025-01-01T00:00:00Z",
                end_rotations_at="2025-12-31T23:59:59Z",
            )

        self.assertIn("API not set", str(context.exception))


class TestOnCallEvent(unittest.TestCase):
    """Tests for the OnCallEvent class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.event_data = {
            "id": "56789",
            "type": "on_call_event",
            "attributes": {
                "starts_at": "2025-01-01T09:00:00Z",
                "ends_at": "2025-01-01T17:00:00Z",
                "users": ["tomas@betterstack.com", "alice@betterstack.com"],
                "override": True,
            },
        }

    def test_create_event_from_response(self):
        """Test creating an OnCallEvent from API response."""
        event = OnCallEvent._from_api_response(self.api, self.event_data)

        self.assertEqual(event.id, "56789")
        self.assertEqual(event.starts_at, "2025-01-01T09:00:00Z")
        self.assertEqual(event.ends_at, "2025-01-01T17:00:00Z")
        self.assertEqual(len(event.users), 2)
        self.assertTrue(event.override)

    def test_generate_url_with_calendar_id(self):
        """Test URL generation for OnCallEvent with calendar_id."""
        event = OnCallEvent._from_api_response(self.api, self.event_data)
        event._calendar_id = "12345"
        self.assertEqual(event.generate_url(), "on-calls/12345/events/56789")

    def test_generate_url_without_calendar_id_raises(self):
        """Test that generate_url raises without calendar_id."""
        event = OnCallEvent._from_api_response(self.api, self.event_data)

        with self.assertRaises(ValueError) as context:
            event.generate_url()

        self.assertIn("calendar_id is required", str(context.exception))

    def test_generate_global_url_raises(self):
        """Test that generate_global_url raises for events."""
        with self.assertRaises(ValueError) as context:
            OnCallEvent.generate_global_url()

        self.assertIn("requires a calendar_id", str(context.exception))

    def test_users_attribute(self):
        """Test that users list is correctly parsed."""
        event = OnCallEvent._from_api_response(self.api, self.event_data)

        self.assertIn("tomas@betterstack.com", event.users)
        self.assertIn("alice@betterstack.com", event.users)
