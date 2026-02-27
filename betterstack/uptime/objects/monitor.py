"""Monitor API objects for BetterStack Uptime.

This module contains the Monitor and MonitorSLA classes for interacting
with the BetterStack Uptime monitoring API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    from ..api import RESTAPI


@dataclass
class Monitor(BaseAPIObject):
    """Monitor resource from the BetterStack Uptime API.

    A monitor represents a URL or service that is being monitored for uptime.
    Monitors can check HTTP endpoints, ping hosts, test TCP/UDP ports, and more.

    Attributes:
        url: The URL of your website or the host you want to ping.
        pronounceable_name: Human-readable name used in phone call alerts.
        monitor_type: Type of monitor (e.g., 'status', 'keyword', 'ping', 'tcp').
        monitor_group_id: ID of the monitor group this monitor belongs to.
        last_checked_at: When the monitor was last checked (ISO 8601 datetime).
        status: Current status (e.g., 'up', 'down', 'paused', 'maintenance').
        policy_id: The escalation policy ID for this monitor.
        expiration_policy_id: The expiration escalation policy ID.
        team_name: The team this monitor is in.
        required_keyword: Keyword that must be present (for keyword/udp monitors).
        verify_ssl: Whether to verify SSL certificate validity.
        check_frequency: How often to check, in seconds.
        call: Whether to call the on-call person on incidents.
        sms: Whether to send SMS on incidents.
        email: Whether to send email on incidents.
        push: Whether to send push notifications on incidents.
        critical_alert: Whether to send critical alert push notifications.
        team_wait: Seconds to wait before escalating to the team.
        http_method: HTTP method for requests (e.g., 'GET', 'POST').
        request_timeout: Request timeout in seconds (or ms for server monitors).
        recovery_period: Seconds before marking incident as resolved after recovery.
        request_headers: Array of custom HTTP headers with 'name' and 'value' properties.
        request_body: Request body for POST/PUT/PATCH, or domain for DNS monitors.
        paused_at: When the monitor was paused (ISO 8601 datetime), null if not paused.
        created_at: When the monitor was created (ISO 8601 datetime).
        updated_at: When the monitor was last updated (ISO 8601 datetime).
        ssl_expiration: Days before SSL expiration to alert.
        domain_expiration: Days before domain expiration to alert.
        regions: Array of regions to check from (e.g., 'us', 'eu', 'as', 'au').
        port: Port for TCP/UDP/SMTP/POP/IMAP monitors.
        confirmation_period: Seconds to wait after failure before starting incident.
        expected_status_codes: Array of acceptable HTTP status codes.
        maintenance_days: Array of maintenance days (e.g., 'mon', 'tue', 'wed').
        maintenance_from: Start of daily maintenance window (e.g., '01:00:00').
        maintenance_to: End of daily maintenance window (e.g., '03:00:00').
        maintenance_timezone: Timezone for maintenance window.
        playwright_script: JavaScript source code for Playwright monitors.
        environment_variables: Environment variables for Playwright scenarios.
        auth_username: Basic auth username.
        auth_password: Basic auth password.
        follow_redirects: Whether to follow HTTP redirects.
        remember_cookies: Whether to remember cookies between checks.
    """

    type: ClassVar[str] = "monitor"
    _url_endpoint: ClassVar[str] = "monitors"
    _allowed_query_parameters: ClassVar[list[str]] = [
        "url",
        "pronounceable_name",
        "per_page",
        "team_name",
    ]

    # Known fields with types
    url: str | None = None
    pronounceable_name: str | None = None
    monitor_type: str | None = None
    monitor_group_id: int | None = None
    last_checked_at: str | None = None
    status: str | None = None
    policy_id: int | None = None
    expiration_policy_id: int | None = None
    team_name: str | None = None
    required_keyword: str | None = None
    verify_ssl: bool | None = None
    check_frequency: int | None = None
    call: bool | None = None
    sms: bool | None = None
    email: bool | None = None
    push: bool | None = None
    critical_alert: bool | None = None
    team_wait: int | None = None
    http_method: str | None = None
    request_timeout: int | None = None
    recovery_period: int | None = None
    request_headers: list[dict[str, str]] | None = None
    request_body: str | None = None
    paused_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    ssl_expiration: int | None = None
    domain_expiration: int | None = None
    regions: list[str] | None = None
    port: str | None = None
    confirmation_period: int | None = None
    expected_status_codes: list[int] | None = None
    maintenance_days: list[str] | None = None
    maintenance_from: str | None = None
    maintenance_to: str | None = None
    maintenance_timezone: str | None = None
    playwright_script: str | None = None
    environment_variables: dict[str, Any] | None = None
    auth_username: str | None = None
    auth_password: str | None = None
    follow_redirects: bool | None = None
    remember_cookies: bool | None = None

    # Private fields for lazy-loaded relationships
    _sla: MonitorSLA | None = field(default=None, repr=False, compare=False)

    @property
    def sla(self) -> MonitorSLA:
        """Get or create the SLA object for this monitor.

        Returns:
            MonitorSLA object for this monitor.
        """
        if self._sla is None:
            self._sla = MonitorSLA(id=self.id, _api=self._api)
        return self._sla

    @property
    def is_paused(self) -> bool:
        """Check if the monitor is currently paused.

        Returns:
            True if the monitor is paused, False otherwise.
        """
        return self.paused_at is not None


@dataclass
class MonitorSLA(BaseAPIObject):
    """Monitor SLA (Service Level Agreement) data.

    This object provides SLA statistics for a specific monitor
    over a given time period.

    Attributes:
        availability: Availability percentage (0-100).
        downtime_duration: Total downtime in seconds.
        number_of_incidents: Number of incidents in the period.
        longest_incident: Duration of longest incident in seconds.
        average_incident: Average incident duration in seconds.
    """

    type: ClassVar[str] = "monitor_sla"
    _url_endpoint: ClassVar[str] = "monitors/{id}/sla"
    _allowed_query_parameters: ClassVar[list[str]] = ["from", "to"]

    # Known fields with types
    availability: float | None = None
    downtime_duration: int | None = None
    number_of_incidents: int | None = None
    longest_incident: int | None = None
    average_incident: int | None = None

    # Private fields for timeframe
    _sla_start: str | None = field(default=None, repr=False, compare=False)
    _sla_end: str | None = field(default=None, repr=False, compare=False)

    def generate_url(self) -> str:
        """Create the URL for this SLA endpoint.

        Returns:
            Full SLA URL path.
        """
        return f"monitors/{self.id}/sla"

    @classmethod
    def generate_global_url(cls) -> str:
        """SLA objects don't have a global URL.

        Raises:
            ValueError: Always, as SLA has no collection endpoint.
        """
        raise ValueError("No overview available for SLA objects")

    @property
    def timeframe(self) -> tuple[str | None, str | None]:
        """Get the current SLA timeframe.

        Returns:
            Tuple of (start_date, end_date).
        """
        return (self._sla_start, self._sla_end)

    @timeframe.setter
    def timeframe(self, frame: tuple[str, str]) -> None:
        """Set the SLA timeframe and fetch new data.

        Args:
            frame: Tuple of (start_date, end_date) in ISO 8601 format.
        """
        start, end = frame
        self._sla_start = start
        self._sla_end = end
        self.fetch_data(from_=start, to=end)

    def fetch_sla(self, from_date: str, to_date: str) -> None:
        """Fetch SLA data for a specific time period.

        Args:
            from_date: Start date in ISO 8601 format.
            to_date: End date in ISO 8601 format.
        """
        self.timeframe = (from_date, to_date)
