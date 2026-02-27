"""Tests for EscalationPolicy and PolicyStep."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import EscalationPolicy, PolicyStep

from .fixtures import make_paginated_response


class TestEscalationPolicy(unittest.TestCase):
    """Tests for the EscalationPolicy class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.policy_data = {
            "id": "456789",
            "type": "policy",
            "attributes": {
                "name": "Standard Escalation Policy",
                "repeat_count": 3,
                "repeat_delay": 1800,
                "incident_token": "AND63ccyT18oKcSFnbJfxlFi1",
                "policy_group_id": None,
                "team_name": "Test Team",
                "steps": [
                    {
                        "type": "escalation",
                        "urgency_id": 123456,
                        "step_members": [{"type": "current_on_call"}],
                        "wait_before": 0,
                    },
                    {
                        "type": "escalation",
                        "urgency_id": 123456,
                        "step_members": [{"type": "entire_team"}],
                        "wait_before": 600,
                    },
                ],
            },
        }

    def test_create_policy_from_response(self):
        """Test creating an EscalationPolicy from API response."""
        policy = EscalationPolicy._from_api_response(self.api, self.policy_data)

        self.assertEqual(policy.id, "456789")
        self.assertEqual(policy.type, "policy")
        self.assertEqual(policy.name, "Standard Escalation Policy")
        self.assertEqual(policy.repeat_count, 3)
        self.assertEqual(policy.repeat_delay, 1800)
        self.assertEqual(policy.incident_token, "AND63ccyT18oKcSFnbJfxlFi1")
        self.assertEqual(policy.team_name, "Test Team")
        self.assertIsNone(policy.policy_group_id)

    def test_steps_attribute(self):
        """Test that steps are correctly parsed."""
        policy = EscalationPolicy._from_api_response(self.api, self.policy_data)

        self.assertIsNotNone(policy.steps)
        self.assertEqual(len(policy.steps), 2)
        self.assertEqual(policy.steps[0]["type"], "escalation")
        self.assertEqual(policy.steps[0]["wait_before"], 0)
        self.assertEqual(policy.steps[1]["wait_before"], 600)

    def test_generate_url(self):
        """Test URL generation for EscalationPolicy."""
        policy = EscalationPolicy._from_api_response(self.api, self.policy_data)
        # Uses v3 API via relative path
        self.assertEqual(policy.generate_url(), "../v3/policies/456789")

    def test_generate_global_url(self):
        """Test global URL generation for EscalationPolicy."""
        self.assertEqual(EscalationPolicy.generate_global_url(), "../v3/policies")

    @responses.activate
    def test_get_all_policies(self):
        """Test fetching all escalation policies."""
        # The v3 endpoint URL
        responses.add(
            responses.GET,
            "https://uptime.betterstack.com/api/v3/policies",
            json=make_paginated_response([self.policy_data]),
            status=200,
        )

        policies = list(EscalationPolicy.get_all_instances(self.api))

        self.assertEqual(len(policies), 1)
        self.assertEqual(policies[0].name, "Standard Escalation Policy")

    def test_time_branching_steps(self):
        """Test policy with time branching steps."""
        branching_data = {
            "id": "789",
            "type": "policy",
            "attributes": {
                "name": "Time-Based Policy",
                "repeat_count": 3,
                "repeat_delay": 60,
                "incident_token": "token123",
                "policy_group_id": None,
                "team_name": "Production",
                "steps": [
                    {
                        "type": "time_branching",
                        "wait_before": 0,
                        "timezone": "Prague",
                        "days": ["mon", "tue", "wed", "thu", "fri"],
                        "time_from": "00:00",
                        "time_to": "00:00",
                        "policy_id": 456,
                    },
                    {
                        "type": "time_branching",
                        "wait_before": 0,
                        "timezone": "Prague",
                        "days": ["sat", "sun"],
                        "time_from": "00:00",
                        "time_to": "00:00",
                        "policy_metadata_key": "Weekend-policy",
                    },
                ],
            },
        }

        policy = EscalationPolicy._from_api_response(self.api, branching_data)

        self.assertEqual(len(policy.steps), 2)
        self.assertEqual(policy.steps[0]["type"], "time_branching")
        self.assertEqual(policy.steps[0]["days"], ["mon", "tue", "wed", "thu", "fri"])
        self.assertEqual(policy.steps[1]["days"], ["sat", "sun"])


class TestPolicyStep(unittest.TestCase):
    """Tests for the PolicyStep helper class."""

    def test_escalation_step_to_dict(self):
        """Test converting an escalation step to dictionary."""
        step = PolicyStep(
            step_type="escalation",
            wait_before=0,
            urgency_id=123456,
            step_members=[{"type": "current_on_call"}],
        )

        result = step.to_dict()

        self.assertEqual(result["type"], "escalation")
        self.assertEqual(result["wait_before"], 0)
        self.assertEqual(result["urgency_id"], 123456)
        self.assertEqual(result["step_members"], [{"type": "current_on_call"}])

    def test_escalation_step_defaults(self):
        """Test escalation step with default values."""
        step = PolicyStep()

        result = step.to_dict()

        self.assertEqual(result["type"], "escalation")
        self.assertEqual(result["wait_before"], 0)
        self.assertNotIn("urgency_id", result)
        self.assertNotIn("step_members", result)

    def test_time_branching_step_to_dict(self):
        """Test converting a time branching step to dictionary."""
        step = PolicyStep(
            step_type="time_branching",
            wait_before=0,
            timezone="Prague",
            days=["mon", "tue", "wed"],
            time_from="09:00",
            time_to="17:00",
            policy_id=456,
        )

        result = step.to_dict()

        self.assertEqual(result["type"], "time_branching")
        self.assertEqual(result["wait_before"], 0)
        self.assertEqual(result["timezone"], "Prague")
        self.assertEqual(result["days"], ["mon", "tue", "wed"])
        self.assertEqual(result["time_from"], "09:00")
        self.assertEqual(result["time_to"], "17:00")
        self.assertEqual(result["policy_id"], 456)
        self.assertNotIn("policy_metadata_key", result)

    def test_time_branching_with_metadata_key(self):
        """Test time branching step with metadata key instead of policy_id."""
        step = PolicyStep(
            step_type="time_branching",
            wait_before=0,
            timezone="UTC",
            days=["sat", "sun"],
            time_from="00:00",
            time_to="23:59",
            policy_metadata_key="weekend-policy",
        )

        result = step.to_dict()

        self.assertEqual(result["type"], "time_branching")
        self.assertEqual(result["policy_metadata_key"], "weekend-policy")
        self.assertNotIn("policy_id", result)

    def test_escalation_step_does_not_include_time_fields(self):
        """Test that escalation steps don't include time branching fields."""
        step = PolicyStep(
            step_type="escalation",
            wait_before=600,
            urgency_id=789,
            step_members=[{"type": "entire_team"}],
            # These should be ignored for escalation type
            timezone="Prague",
            days=["mon"],
        )

        result = step.to_dict()

        self.assertNotIn("timezone", result)
        self.assertNotIn("days", result)
        self.assertNotIn("time_from", result)
        self.assertNotIn("time_to", result)
