"""Incident API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from ..base import BaseAPIObject


@dataclass
class Incident(BaseAPIObject):
    """Incident resource from the BetterStack Uptime API (v3).

    An incident represents a period of downtime or issues detected
    by a monitor or heartbeat. Incidents are automatically created when
    a monitor or heartbeat fails and can be acknowledged and resolved
    manually or automatically.

    Note:
        This resource uses the v3 API endpoint (``/api/v3/incidents``).

    Attributes:
        name: The name/title of the incident.
        url: The URL that triggered the incident (for URL monitors).
        http_method: The HTTP method used when the incident was detected.
        cause: The cause of the incident (e.g., "Keyword not found").
        incident_group_id: ID of the incident group this incident belongs to.
        started_at: When the incident started (ISO 8601 format).
        acknowledged_at: When the incident was acknowledged (ISO 8601 format).
        acknowledged_by: Name of who acknowledged the incident.
        resolved_at: When the incident was resolved (ISO 8601 format).
        resolved_by: Name of who resolved the incident.
        status: Current status of the incident (e.g., "Started", "Resolved").
        team_name: The team that owns this incident (for filtering).
        response_content: The response body content when the incident occurred.
        response_url: The final URL after any redirects.
        response_options: Additional response information/options.
        regions: List of regions where the incident was detected.
        screenshot_url: URL to a screenshot taken during the incident.
        origin_url: The original URL before any redirects.
        escalation_policy_id: ID of the escalation policy that was triggered.
        ssl_certificate_expires_at: When the SSL certificate expires.
        domain_expires_at: When the domain expires.
        call: Whether phone calls were made for this incident.
        sms: Whether SMS was sent for this incident.
        email: Whether email was sent for this incident.
        push: Whether push notifications were sent for this incident.
        critical_alert: Whether critical/high-urgency alerts were sent.
        metadata: Custom metadata dictionary attached to this incident.
        monitor_id: ID of the monitor that triggered this incident.
        heartbeat_id: ID of the heartbeat that triggered this incident.
    """

    type: ClassVar[str] = "incident"
    _url_endpoint: ClassVar[str] = "../v3/incidents"
    _allowed_query_parameters: ClassVar[list[str]] = [
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

    # Known fields
    name: str | None = None
    url: str | None = None
    http_method: str | None = None
    cause: str | None = None
    incident_group_id: int | None = None
    started_at: str | None = None
    acknowledged_at: str | None = None
    acknowledged_by: str | None = None
    resolved_at: str | None = None
    resolved_by: str | None = None
    status: str | None = None
    team_name: str | None = None
    response_content: str | None = None
    response_url: str | None = None
    response_options: dict[str, Any] | None = None
    regions: list[str] | None = None
    screenshot_url: str | None = None
    origin_url: str | None = None
    escalation_policy_id: int | None = None
    ssl_certificate_expires_at: str | None = None
    domain_expires_at: str | None = None
    call: bool | None = None
    sms: bool | None = None
    email: bool | None = None
    push: bool | None = None
    critical_alert: bool | None = None
    metadata: dict[str, Any] | None = None
    monitor_id: int | None = None
    heartbeat_id: int | None = None

    @property
    def is_resolved(self) -> bool:
        """Check if the incident has been resolved.

        Returns:
            True if the incident has a resolved_at timestamp or
            status is "Resolved".
        """
        return self.resolved_at is not None or self.status == "Resolved"

    @property
    def is_acknowledged(self) -> bool:
        """Check if the incident has been acknowledged.

        Returns:
            True if the incident has an acknowledged_at timestamp or
            status is "Acknowledged".
        """
        return self.acknowledged_at is not None or self.status == "Acknowledged"

    def acknowledge(self, acknowledged_by: str | None = None) -> None:
        """Acknowledge this incident.

        Acknowledging an incident indicates that someone is aware of
        the issue and is working on it. This stops further escalations.

        Args:
            acknowledged_by: Optional name of who is acknowledging
                the incident.
        """
        body = {}
        if acknowledged_by:
            body["acknowledged_by"] = acknowledged_by

        response = self._api.post(f"{self.generate_url()}/acknowledge", body=body)
        response_data = response.json()

        # Update local state with response
        for key, value in response_data.get("data", {}).get("attributes", {}).items():
            self._set_attribute(key, value)
        self.reset_variable_tracking()

    def resolve(self, resolved_by: str | None = None) -> None:
        """Resolve this incident.

        Resolving an incident marks it as fixed. This stops all
        notifications and escalations for this incident.

        Args:
            resolved_by: Optional name of who is resolving the incident.
        """
        body = {}
        if resolved_by:
            body["resolved_by"] = resolved_by

        response = self._api.post(f"{self.generate_url()}/resolve", body=body)
        response_data = response.json()

        # Update local state with response
        for key, value in response_data.get("data", {}).get("attributes", {}).items():
            self._set_attribute(key, value)
        self.reset_variable_tracking()
