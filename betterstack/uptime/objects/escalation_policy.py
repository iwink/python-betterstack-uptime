"""EscalationPolicy API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    pass


@dataclass
class EscalationPolicy(BaseAPIObject):
    """EscalationPolicy resource from the BetterStack Uptime API.

    An escalation policy defines the sequence of notifications sent when
    an incident occurs. It specifies who to notify and in what order.

    Note: This resource uses the v3 API endpoint.

    Attributes:
        name: The name of the policy.
        repeat_count: How many times to repeat the escalation steps.
        repeat_delay: Seconds to wait before each repetition.
        incident_token: Token for manually reporting incidents.
        policy_group_id: ID of the policy group.
        team_name: Name of the team that owns the policy.
        steps: List of escalation steps.
    """

    type: ClassVar[str] = "policy"
    # Use relative path to go from v2 to v3
    _url_endpoint: ClassVar[str] = "../v3/policies"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page", "team_name"]

    # Known fields with types
    name: str | None = None
    repeat_count: int | None = None
    repeat_delay: int | None = None
    incident_token: str | None = None
    policy_group_id: int | None = None
    team_name: str | None = None
    steps: list[dict[str, Any]] | None = None


@dataclass
class PolicyStep:
    """Represents a single step in an escalation policy.

    This is a helper class for constructing escalation policy steps.
    It is not a full API object but can be used when creating policies.

    Attributes:
        step_type: Type of step ('escalation' or 'time_branching').
        wait_before: Seconds to wait before executing this step.
        urgency_id: ID of the urgency level for this step.
        step_members: List of members to notify.
        timezone: Timezone for time branching steps.
        days: Days of the week for time branching.
        time_from: Start time for time branching.
        time_to: End time for time branching.
        policy_id: ID of the policy to branch to.
        policy_metadata_key: Metadata key for the branched policy.
    """

    step_type: str = "escalation"
    wait_before: int = 0
    urgency_id: int | None = None
    step_members: list[dict[str, str]] | None = None
    # Time branching fields
    timezone: str | None = None
    days: list[str] | None = None
    time_from: str | None = None
    time_to: str | None = None
    policy_id: int | None = None
    policy_metadata_key: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert step to dictionary for API requests.

        Returns:
            Dictionary representation of the step.
        """
        result: dict[str, Any] = {
            "type": self.step_type,
            "wait_before": self.wait_before,
        }

        if self.step_type == "escalation":
            if self.urgency_id is not None:
                result["urgency_id"] = self.urgency_id
            if self.step_members is not None:
                result["step_members"] = self.step_members
        elif self.step_type == "time_branching":
            if self.timezone is not None:
                result["timezone"] = self.timezone
            if self.days is not None:
                result["days"] = self.days
            if self.time_from is not None:
                result["time_from"] = self.time_from
            if self.time_to is not None:
                result["time_to"] = self.time_to
            if self.policy_id is not None:
                result["policy_id"] = self.policy_id
            if self.policy_metadata_key is not None:
                result["policy_metadata_key"] = self.policy_metadata_key

        return result
