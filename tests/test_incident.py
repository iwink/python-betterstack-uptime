"""Tests for Incident API object."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Incident
from tests.fixtures import V3_BASE_URL, make_paginated_response


# Incident fixture data (v3 API format)
INCIDENT_1 = {
    "data": {
        "id": "1",
        "type": "incident",
        "attributes": {
            "name": "Test Incident",
            "url": "https://example.com",
            "http_method": "get",
            "cause": "timeout",
            "incident_group_id": None,
            "started_at": "2023-05-08T00:00:00.000Z",
            "resolved_at": None,
            "acknowledged_at": None,
            "acknowledged_by": None,
            "resolved_by": None,
            "status": "Started",
            "team_name": "Engineering",
            "response_content": None,
            "response_url": "https://example.com",
            "response_options": None,
            "regions": ["us", "eu"],
            "origin_url": "https://example.com",
            "escalation_policy_id": 456,
            "ssl_certificate_expires_at": None,
            "domain_expires_at": None,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "critical_alert": False,
            "metadata": {"key": "value"},
            "screenshot_url": None,
            "monitor_id": 123,
            "heartbeat_id": None,
        },
    }
}

INCIDENT_ACKNOWLEDGED = {
    "data": {
        "id": "1",
        "type": "incident",
        "attributes": {
            "name": "Test Incident",
            "url": "https://example.com",
            "http_method": "get",
            "cause": "timeout",
            "incident_group_id": None,
            "started_at": "2023-05-08T00:00:00.000Z",
            "resolved_at": None,
            "acknowledged_at": "2023-05-08T01:00:00.000Z",
            "acknowledged_by": "admin",
            "resolved_by": None,
            "status": "Acknowledged",
            "team_name": "Engineering",
            "response_content": None,
            "response_url": "https://example.com",
            "response_options": None,
            "regions": ["us", "eu"],
            "origin_url": "https://example.com",
            "escalation_policy_id": 456,
            "ssl_certificate_expires_at": None,
            "domain_expires_at": None,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "critical_alert": False,
            "metadata": {"key": "value"},
            "screenshot_url": None,
            "monitor_id": 123,
            "heartbeat_id": None,
        },
    }
}

INCIDENT_RESOLVED = {
    "data": {
        "id": "1",
        "type": "incident",
        "attributes": {
            "name": "Test Incident",
            "url": "https://example.com",
            "http_method": "get",
            "cause": "timeout",
            "incident_group_id": None,
            "started_at": "2023-05-08T00:00:00.000Z",
            "resolved_at": "2023-05-08T02:00:00.000Z",
            "acknowledged_at": "2023-05-08T01:00:00.000Z",
            "acknowledged_by": "admin",
            "resolved_by": "admin",
            "status": "Resolved",
            "team_name": "Engineering",
            "response_content": None,
            "response_url": "https://example.com",
            "response_options": None,
            "regions": ["us", "eu"],
            "origin_url": "https://example.com",
            "escalation_policy_id": 456,
            "ssl_certificate_expires_at": None,
            "domain_expires_at": None,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "critical_alert": False,
            "metadata": {"key": "value"},
            "screenshot_url": None,
            "monitor_id": 123,
            "heartbeat_id": None,
        },
    }
}


class TestIncident(unittest.TestCase):
    """Tests for Incident class operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")

    @responses.activate
    def test_get_all_incidents(self):
        """Test fetching all incidents uses v3 API."""
        responses.add(
            responses.GET,
            f"{V3_BASE_URL}incidents",
            json=make_paginated_response([INCIDENT_1["data"]]),
            status=200,
        )

        incidents = list(Incident.get_all_instances(self.api))

        self.assertEqual(len(incidents), 1)
        self.assertEqual(incidents[0].name, "Test Incident")
        self.assertEqual(incidents[0].cause, "timeout")

    def test_is_resolved_false(self):
        """Test is_resolved property when incident is not resolved."""
        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])

        self.assertFalse(incident.is_resolved)

    def test_is_resolved_true_by_timestamp(self):
        """Test is_resolved property when incident has resolved_at timestamp."""
        incident = Incident._from_api_response(self.api, INCIDENT_RESOLVED["data"])

        self.assertTrue(incident.is_resolved)

    def test_is_resolved_true_by_status(self):
        """Test is_resolved property when incident status is Resolved."""
        data = INCIDENT_1["data"].copy()
        data["attributes"] = INCIDENT_1["data"]["attributes"].copy()
        data["attributes"]["status"] = "Resolved"
        incident = Incident._from_api_response(self.api, data)

        self.assertTrue(incident.is_resolved)

    def test_is_acknowledged_false(self):
        """Test is_acknowledged property when incident is not acknowledged."""
        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])

        self.assertFalse(incident.is_acknowledged)

    def test_is_acknowledged_true_by_timestamp(self):
        """Test is_acknowledged property when incident has acknowledged_at timestamp."""
        incident = Incident._from_api_response(self.api, INCIDENT_ACKNOWLEDGED["data"])

        self.assertTrue(incident.is_acknowledged)

    def test_is_acknowledged_true_by_status(self):
        """Test is_acknowledged property when incident status is Acknowledged."""
        data = INCIDENT_1["data"].copy()
        data["attributes"] = INCIDENT_1["data"]["attributes"].copy()
        data["attributes"]["status"] = "Acknowledged"
        incident = Incident._from_api_response(self.api, data)

        self.assertTrue(incident.is_acknowledged)

    @responses.activate
    def test_acknowledge_incident(self):
        """Test acknowledging an incident."""
        responses.add(
            responses.POST,
            f"{V3_BASE_URL}incidents/1/acknowledge",
            json=INCIDENT_ACKNOWLEDGED,
            status=200,
        )

        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])
        incident.acknowledge(acknowledged_by="admin")

        self.assertEqual(incident.acknowledged_at, "2023-05-08T01:00:00.000Z")
        self.assertEqual(incident.acknowledged_by, "admin")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_acknowledge_incident_without_name(self):
        """Test acknowledging an incident without specifying who."""
        responses.add(
            responses.POST,
            f"{V3_BASE_URL}incidents/1/acknowledge",
            json=INCIDENT_ACKNOWLEDGED,
            status=200,
        )

        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])
        incident.acknowledge()

        self.assertTrue(incident.is_acknowledged)

    @responses.activate
    def test_resolve_incident(self):
        """Test resolving an incident."""
        responses.add(
            responses.POST,
            f"{V3_BASE_URL}incidents/1/resolve",
            json=INCIDENT_RESOLVED,
            status=200,
        )

        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])
        incident.resolve(resolved_by="admin")

        self.assertEqual(incident.resolved_at, "2023-05-08T02:00:00.000Z")
        self.assertEqual(incident.resolved_by, "admin")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_resolve_incident_without_name(self):
        """Test resolving an incident without specifying who."""
        responses.add(
            responses.POST,
            f"{V3_BASE_URL}incidents/1/resolve",
            json=INCIDENT_RESOLVED,
            status=200,
        )

        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])
        incident.resolve()

        self.assertTrue(incident.is_resolved)

    @responses.activate
    def test_filter_incidents_by_monitor(self):
        """Test filtering incidents by monitor_id."""
        responses.add(
            responses.GET,
            f"{V3_BASE_URL}incidents",
            json=make_paginated_response([INCIDENT_1["data"]]),
            status=200,
        )

        incidents = list(Incident.filter(self.api, monitor_id=123))

        self.assertEqual(len(incidents), 1)
        self.assertIn("monitor_id=123", responses.calls[0].request.url)

    @responses.activate
    def test_filter_incidents_by_team_name(self):
        """Test filtering incidents by team_name (v3 feature)."""
        responses.add(
            responses.GET,
            f"{V3_BASE_URL}incidents",
            json=make_paginated_response([INCIDENT_1["data"]]),
            status=200,
        )

        incidents = list(Incident.filter(self.api, team_name="Engineering"))

        self.assertEqual(len(incidents), 1)
        self.assertIn("team_name=Engineering", responses.calls[0].request.url)

    @responses.activate
    def test_filter_incidents_by_resolved(self):
        """Test filtering incidents by resolved status (v3 feature)."""
        responses.add(
            responses.GET,
            f"{V3_BASE_URL}incidents",
            json=make_paginated_response([INCIDENT_RESOLVED["data"]]),
            status=200,
        )

        incidents = list(Incident.filter(self.api, resolved=True))

        self.assertEqual(len(incidents), 1)
        self.assertIn("resolved=True", responses.calls[0].request.url)

    @responses.activate
    def test_filter_incidents_by_acknowledged(self):
        """Test filtering incidents by acknowledged status (v3 feature)."""
        responses.add(
            responses.GET,
            f"{V3_BASE_URL}incidents",
            json=make_paginated_response([INCIDENT_ACKNOWLEDGED["data"]]),
            status=200,
        )

        incidents = list(Incident.filter(self.api, acknowledged=True))

        self.assertEqual(len(incidents), 1)
        self.assertIn("acknowledged=True", responses.calls[0].request.url)

    def test_v3_attributes_present(self):
        """Test that v3 API attributes are properly parsed."""
        incident = Incident._from_api_response(self.api, INCIDENT_1["data"])

        # Test v3 specific attributes
        self.assertEqual(incident.status, "Started")
        self.assertEqual(incident.team_name, "Engineering")
        self.assertEqual(incident.regions, ["us", "eu"])
        self.assertEqual(incident.escalation_policy_id, 456)
        self.assertEqual(incident.origin_url, "https://example.com")
        self.assertEqual(incident.response_url, "https://example.com")
        self.assertEqual(incident.critical_alert, False)
        self.assertEqual(incident.metadata, {"key": "value"})

    def test_endpoint_uses_v3(self):
        """Test that the Incident class uses the v3 API endpoint."""
        self.assertEqual(Incident._url_endpoint, "../v3/incidents")

    def test_allowed_query_parameters_include_v3(self):
        """Test that v3 query parameters are available."""
        expected_params = [
            "from",
            "to",
            "per_page",
            "monitor_id",
            "heartbeat_id",
            "team_name",
            "resolved",
            "acknowledged",
            "metadata",
        ]
        self.assertEqual(Incident._allowed_query_parameters, expected_params)
