"""Tests for MonitorSLA API object."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Monitor, MonitorSLA
from tests.fixtures import BASE_URL, MONITOR_1

# MonitorSLA fixture data - single object response (not paginated)
SLA_RESPONSE = {
    "data": {
        "id": "1",
        "type": "monitor_sla",
        "attributes": {
            "availability": 99.95,
            "downtime_duration": 1800,
            "number_of_incidents": 2,
            "longest_incident": 1200,
            "average_incident": 900,
        },
    }
}


class TestMonitorSLA(unittest.TestCase):
    """Tests for MonitorSLA class operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    def test_create_monitor_sla(self):
        """Test creating a MonitorSLA object."""
        sla = MonitorSLA(id=1, _api=self.api)

        self.assertEqual(sla.id, 1)
        self.assertIsNone(sla.availability)
        self.assertIsNone(sla.downtime_duration)

    def test_generate_url(self):
        """Test URL generation for MonitorSLA."""
        sla = MonitorSLA(id=123, _api=self.api)

        self.assertEqual(sla.generate_url(), "monitors/123/sla")

    def test_generate_global_url_raises(self):
        """Test that generate_global_url raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            MonitorSLA.generate_global_url()

        self.assertIn("No overview available", str(ctx.exception))

    def test_timeframe_property_initial(self):
        """Test timeframe property returns None values initially."""
        sla = MonitorSLA(id=1, _api=self.api)

        start, end = sla.timeframe

        self.assertIsNone(start)
        self.assertIsNone(end)

    @responses.activate
    def test_timeframe_setter_fetches_data(self):
        """Test that setting timeframe fetches SLA data."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1/sla",
            json=SLA_RESPONSE,
            status=200,
        )

        sla = MonitorSLA(id=1, _api=self.api)
        sla.timeframe = ("2023-01-01T00:00:00Z", "2023-01-31T23:59:59Z")

        self.assertEqual(sla.availability, 99.95)
        self.assertEqual(sla.downtime_duration, 1800)
        self.assertEqual(sla.number_of_incidents, 2)
        self.assertEqual(sla.longest_incident, 1200)
        self.assertEqual(sla.average_incident, 900)
        self.assertEqual(sla.timeframe, ("2023-01-01T00:00:00Z", "2023-01-31T23:59:59Z"))
        self.assertEqual(len(responses.calls), 1)
        # Check that parameters were passed correctly (from_ becomes from in URL)
        self.assertIn("from=2023-01-01", responses.calls[0].request.url)
        self.assertIn("to=2023-01-31", responses.calls[0].request.url)

    @responses.activate
    def test_fetch_sla_method(self):
        """Test fetch_sla method fetches data for the given period."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1/sla",
            json=SLA_RESPONSE,
            status=200,
        )

        sla = MonitorSLA(id=1, _api=self.api)
        sla.fetch_sla("2023-06-01T00:00:00Z", "2023-06-30T23:59:59Z")

        self.assertEqual(sla.availability, 99.95)
        self.assertEqual(sla.timeframe, ("2023-06-01T00:00:00Z", "2023-06-30T23:59:59Z"))
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_from_api_response(self):
        """Test creating MonitorSLA from API response."""
        sla = MonitorSLA._from_api_response(self.api, SLA_RESPONSE["data"])

        self.assertEqual(sla.id, "1")
        self.assertEqual(sla.availability, 99.95)
        self.assertEqual(sla.downtime_duration, 1800)
        self.assertEqual(sla.number_of_incidents, 2)


class TestMonitorSLAProperty(unittest.TestCase):
    """Tests for Monitor.sla property."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    def test_monitor_sla_property_returns_sla_object(self):
        """Test that Monitor.sla property returns MonitorSLA object."""
        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])

        sla = monitor.sla

        self.assertIsInstance(sla, MonitorSLA)
        self.assertEqual(sla.id, monitor.id)

    def test_monitor_sla_property_caching(self):
        """Test that Monitor.sla property returns same object on subsequent calls."""
        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])

        sla_first = monitor.sla
        sla_second = monitor.sla

        self.assertIs(sla_first, sla_second)

    @responses.activate
    def test_monitor_sla_fetch_data(self):
        """Test fetching SLA data through Monitor.sla property."""
        responses.add(
            responses.GET,
            f"{BASE_URL}monitors/1/sla",
            json=SLA_RESPONSE,
            status=200,
        )

        monitor = Monitor._from_api_response(self.api, MONITOR_1["data"])
        monitor.sla.fetch_sla("2023-01-01T00:00:00Z", "2023-01-31T23:59:59Z")

        self.assertEqual(monitor.sla.availability, 99.95)
        self.assertEqual(monitor.sla.number_of_incidents, 2)
