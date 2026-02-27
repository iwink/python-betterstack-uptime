"""Tests for BaseAPIObject and Monitor classes."""

import copy
import unittest
from unittest import mock

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.exceptions import ValidationError
from betterstack.uptime.objects import Monitor, MonitorGroup
from tests.fixtures import (
    BASE_URL,
    MONITOR_1,
    MONITOR_2,
    MONITOR_3,
    make_paginated_response,
)


class TestMonitor(unittest.TestCase):
    """Tests for Monitor class operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    @responses.activate
    def test_get_existing(self):
        """Test fetching an existing monitor by ID."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1",
            json=MONITOR_1,
            status=200,
        )

        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])

        self.assertEqual(monitor.url, "https://example.com")
        self.assertEqual(monitor.pronounceable_name, "MyWeirdExampleSite")

    @responses.activate
    def test_get_all_instances(self):
        """Test fetching all monitor instances."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([MONITOR_1["data"], MONITOR_2["data"]]),
            status=200,
        )

        monitors = list(Monitor.get_all_instances(self.api))

        self.assertEqual(len(monitors), 2)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_modify_single_value(self):
        """Test modifying a single value and saving."""
        # Initial GET for the monitor
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1",
            json=MONITOR_1,
            status=200,
        )

        # PATCH response with updated data
        updated_monitor = copy.deepcopy(MONITOR_1)
        updated_monitor["data"]["attributes"]["paused"] = True
        updated_monitor["data"]["attributes"]["updated_at"] = "1970-01-01T00:00:00.000Z"

        responses.add(
            responses.PATCH,
            f"{BASE_URL}monitors/1",
            json=updated_monitor,
            status=200,
        )

        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])
        monitor.paused = True

        self.assertEqual(monitor.get_modified_properties(), ["paused"])
        self.assertTrue(monitor.paused)

        monitor.save()

        self.assertTrue(monitor.paused)
        self.assertEqual(monitor.get_modified_properties(), [])
        self.assertEqual(monitor.updated_at, "1970-01-01T00:00:00.000Z")

    @responses.activate
    def test_monitor_filter(self):
        """Test filtering monitors by attribute."""
        # Response with filtered data (server-side filtering)
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([MONITOR_1["data"]]),
            status=200,
        )

        filtered_monitors = list(Monitor.filter(self.api, url="https://example.com"))

        self.assertEqual(len(filtered_monitors), 1)
        self.assertEqual(filtered_monitors[0].pronounceable_name, "MyWeirdExampleSite")

    @responses.activate
    def test_monitor_filter_no_results(self):
        """Test filtering monitors with no matching results."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([]),
            status=200,
        )

        filtered_monitors = list(Monitor.filter(self.api, url="https://someexample.com"))

        self.assertEqual(len(filtered_monitors), 0)

    @responses.activate
    def test_get_or_create_existing(self):
        """Test get_or_create returns existing monitor."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([MONITOR_1["data"]]),
            status=200,
        )

        created, monitor = Monitor.get_or_create(self.api, url="https://example.com")

        self.assertFalse(created)
        self.assertEqual(monitor.pronounceable_name, "MyWeirdExampleSite")

    @responses.activate
    def test_get_or_create_new(self):
        """Test get_or_create creates new monitor when not found."""
        # First call - no matching monitors
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([]),
            status=200,
        )

        # POST to create new monitor
        responses.add(
            responses.POST,
            f"{BASE_URL}monitors",
            json=MONITOR_3,
            status=201,
        )

        created, monitor = Monitor.get_or_create(self.api, url="https://thirdexample.com")

        self.assertTrue(created)
        self.assertEqual(monitor.pronounceable_name, "MyThirdExampleSite")

    @responses.activate
    def test_delete_monitor(self):
        """Test deleting a monitor."""
        responses.add(
            responses.DELETE,
            f"{BASE_URL}monitors/1",
            status=204,
        )

        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])
        monitor.delete()

        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_new_monitor(self):
        """Test creating a new monitor using Monitor.new()."""
        responses.add(
            responses.POST,
            f"{BASE_URL}monitors",
            json=MONITOR_3,
            status=201,
        )

        monitor = Monitor.new(self.api, url="https://thirdexample.com", monitor_type="status")

        self.assertEqual(monitor.url, "https://thirdexample.com")
        self.assertEqual(monitor.pronounceable_name, "MyThirdExampleSite")

    @responses.activate
    def test_save_no_changes(self):
        """Test that save() does nothing when there are no changes."""
        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])

        # No changes made, save should not make any API calls
        monitor.save()

        self.assertEqual(len(responses.calls), 0)


class TestBaseAPIObject(unittest.TestCase):
    """Tests for BaseAPIObject functionality."""

    def test_extras_storage(self):
        """Test that unknown attributes are stored in extras."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)

        # Set an unknown attribute
        monitor.unknown_field = "test_value"

        # Should be stored in _extras
        self.assertEqual(monitor._extras.get("unknown_field"), "test_value")
        # Should be accessible via attribute
        self.assertEqual(monitor.unknown_field, "test_value")

    def test_change_tracking(self):
        """Test that changes are properly tracked."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)
        monitor.url = "https://example.com"
        monitor.reset_variable_tracking()

        # No changes yet
        self.assertEqual(monitor.get_modified_properties(), [])

        # Modify a property
        monitor.url = "https://changed.com"
        self.assertIn("url", monitor.get_modified_properties())

    def test_change_tracking_no_false_positive(self):
        """Test that setting same value doesn't trigger change."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)
        monitor.url = "https://example.com"
        monitor.reset_variable_tracking()

        # Set same value
        monitor.url = "https://example.com"
        self.assertEqual(monitor.get_modified_properties(), [])

    def test_generate_url(self):
        """Test URL generation for a monitor instance."""
        api = mock.Mock()
        monitor = Monitor(id=123, _api=api)

        self.assertEqual(monitor.generate_url(), "monitors/123")

    def test_generate_global_url(self):
        """Test global URL generation for Monitor class."""
        self.assertEqual(Monitor.generate_global_url(), "monitors")

    def test_attribute_error_for_unknown(self):
        """Test that accessing unknown attributes raises AttributeError."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)

        with self.assertRaises(AttributeError):
            _ = monitor.nonexistent_attribute

    def test_attribute_error_for_private_attributes(self):
        """Test that accessing undefined private attributes raises AttributeError."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)

        with self.assertRaises(AttributeError):
            _ = monitor._nonexistent_private

    @responses.activate
    def test_fetch_data(self):
        """Test fetch_data updates the object from API."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1",
            json=MONITOR_1,
            status=200,
        )

        api = UptimeAPI("test-token")
        monitor = Monitor(id=1, _api=api)
        monitor.url = "old-url"
        monitor.reset_variable_tracking()

        monitor.fetch_data()

        self.assertEqual(monitor.url, "https://example.com")
        self.assertEqual(monitor.pronounceable_name, "MyWeirdExampleSite")
        # After fetch_data, no changes should be marked
        self.assertEqual(monitor.get_modified_properties(), [])

    def test_validate_query_options_empty_allowed(self):
        """Test validation fails when using unsupported query parameters."""
        # MonitorGroup has limited _allowed_query_parameters (only team_name)
        # Using an unsupported parameter should raise ValidationError
        with self.assertRaises(ValidationError) as ctx:
            MonitorGroup._validate_query_options(name="test")

        self.assertIn("is not a valid query parameter", str(ctx.exception))

    def test_validate_query_options_invalid_parameter(self):
        """Test validation fails for invalid query parameter."""
        # Monitor has _allowed_query_parameters but "invalid_param" is not in it
        with self.assertRaises(ValidationError) as ctx:
            Monitor._validate_query_options(invalid_param="test")

        self.assertIn("is not a valid query parameter", str(ctx.exception))

    @responses.activate
    def test_get_or_create_multiple_matches_raises(self):
        """Test get_or_create raises ValueError when multiple matches found."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors",
            json=make_paginated_response([MONITOR_1["data"], MONITOR_2["data"]]),
            status=200,
        )

        api = UptimeAPI("test-token")

        with self.assertRaises(ValueError) as ctx:
            Monitor.get_or_create(api, url="https://example.com")

        self.assertIn("Multiple matches", str(ctx.exception))

    def test_setattr_during_initialization(self):
        """Test __setattr__ handles initialization edge case gracefully."""
        api = mock.Mock()
        # This tests the path where _extras may not exist yet during __init__
        monitor = Monitor(id=1, _api=api)

        # Setting a known field should work
        monitor.url = "https://test.com"
        self.assertEqual(monitor.url, "https://test.com")

    def test_getattr_extras_not_initialized(self):
        """Test __getattr__ handles case when _extras doesn't exist."""
        api = mock.Mock()
        monitor = Monitor(id=1, _api=api)

        # Access unknown field when _extras exists but field is not in it
        with self.assertRaises(AttributeError):
            _ = monitor.definitely_not_a_field
