"""Heartbeat API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ..base import BaseAPIObject


@dataclass
class Heartbeat(BaseAPIObject):
    """Heartbeat resource from the BetterStack Uptime API.

    A heartbeat monitor expects regular "heartbeat" pings from your
    application. If a ping is not received within the expected period,
    an incident is triggered.

    Attributes:
        name: The name of the heartbeat.
        url: The unique URL to ping for this heartbeat.
        period: Expected time between heartbeats in seconds.
        grace: Grace period in seconds before triggering an incident.
        call: Whether to make phone calls on incidents.
        sms: Whether to send SMS on incidents.
        email: Whether to send emails on incidents.
        push: Whether to send push notifications on incidents.
        critical_alert: Whether to send as a critical/high-urgency alert.
        team_wait: Seconds to wait before escalating to the team.
        heartbeat_group_id: ID of the heartbeat group this belongs to.
        team_name: The team that owns this heartbeat (for filtering).
        sort_index: Sort order for the heartbeat in the dashboard.
        paused_at: When the heartbeat was paused (ISO 8601), if paused.
        created_at: When the heartbeat was created (ISO 8601 format).
        updated_at: When the heartbeat was last updated (ISO 8601 format).
        status: Current status of the heartbeat (e.g., "up", "down", "paused").
        maintenance_from: Start time of the maintenance window (HH:MM:SS format).
        maintenance_to: End time of the maintenance window (HH:MM:SS format).
        maintenance_timezone: Timezone for the maintenance window.
        maintenance_days: List of days for maintenance (e.g., ["mon", "tue"]).
        policy_id: ID of the escalation policy for this heartbeat.
    """

    type: ClassVar[str] = "heartbeat"
    _url_endpoint: ClassVar[str] = "heartbeats"
    _allowed_query_parameters: ClassVar[list[str]] = ["team_name"]

    # Known fields
    name: str | None = None
    url: str | None = None
    period: int | None = None
    grace: int | None = None
    call: bool | None = None
    sms: bool | None = None
    email: bool | None = None
    push: bool | None = None
    critical_alert: bool | None = None
    team_wait: int | None = None
    heartbeat_group_id: int | None = None
    team_name: str | None = None
    sort_index: int | None = None
    paused_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    status: str | None = None
    maintenance_from: str | None = None
    maintenance_to: str | None = None
    maintenance_timezone: str | None = None
    maintenance_days: list[str] | None = None
    policy_id: int | None = None

    @property
    def is_paused(self) -> bool:
        """Check if the heartbeat is currently paused.

        Returns:
            True if the heartbeat has a paused_at timestamp.
        """
        return self.paused_at is not None
