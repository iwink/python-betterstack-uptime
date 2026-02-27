"""OnCallCalendar API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    from ..api import RESTAPI


@dataclass
class OnCallCalendar(BaseAPIObject):
    """OnCallCalendar resource from the BetterStack Uptime API.

    An on-call calendar (schedule) defines who is on-call and when.
    It manages on-call rotations and events for incident response.

    Attributes:
        name: The name of the schedule.
        default_calendar: Whether this is the default calendar for the team.
        team_name: Name of the team associated with the schedule.
    """

    type: ClassVar[str] = "on_call_calendar"
    _url_endpoint: ClassVar[str] = "on-calls"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page", "team_name"]

    # Known fields with types
    name: str | None = None
    default_calendar: bool | None = None
    team_name: str | None = None

    # Private fields for lazy-loaded relationships
    _on_call_users: list[dict[str, Any]] | None = field(default=None, repr=False, compare=False)
    _events: list[OnCallEvent] | None = field(default=None, repr=False, compare=False)

    @classmethod
    def _from_api_response(
        cls,
        api: RESTAPI | None,
        data: dict[str, Any],
    ) -> OnCallCalendar:
        """Create an OnCallCalendar from API response data.

        This override handles the relationships.on_call_users data.

        Args:
            api: API instance for further requests.
            data: Raw API response data.

        Returns:
            OnCallCalendar instance.
        """
        instance = super()._from_api_response(api, data)

        # Extract on_call_users from relationships
        relationships = data.get("relationships", {})
        on_call_users_data = relationships.get("on_call_users", {}).get("data", [])
        instance._on_call_users = on_call_users_data

        return instance

    @property
    def on_call_users(self) -> list[dict[str, Any]]:
        """Get the current on-call users for this calendar.

        Returns:
            List of user data dictionaries.
        """
        if self._on_call_users is None:
            return []
        return self._on_call_users

    @property
    def events(self) -> list[OnCallEvent]:
        """Get the events for this on-call calendar (lazy-loaded).

        Returns:
            List of OnCallEvent objects.
        """
        if self._events is None:
            self._events = self.fetch_events()
        return self._events

    def fetch_events(self) -> list[OnCallEvent]:
        """Fetch all events for this on-call calendar from the API.

        Returns:
            List of OnCallEvent objects.
        """
        if self._api is None:
            raise ValueError("API not set")
        url = f"on-calls/{self.id}/events"
        events = []
        for item in self._api.get(url):
            event = OnCallEvent._from_api_response(self._api, item)
            event._calendar_id = self.id
            events.append(event)
        self._events = events
        return events

    def create_rotation(
        self,
        users: list[str],
        rotation_length: int,
        rotation_period: str,
        start_rotations_at: str,
        end_rotations_at: str,
    ) -> dict[str, Any]:
        """Create an on-call rotation for this calendar.

        Args:
            users: List of email addresses of users to include.
            rotation_length: Length of the rotation period.
            rotation_period: Period type ('hour', 'day', 'week').
            start_rotations_at: Start time in ISO 8601 format.
            end_rotations_at: End time in ISO 8601 format.

        Returns:
            API response data for the created rotation.
        """
        if self._api is None:
            raise ValueError("API not set")
        url = f"on-calls/{self.id}/rotation"
        data = {
            "users": users,
            "rotation_length": rotation_length,
            "rotation_period": rotation_period,
            "start_rotations_at": start_rotations_at,
            "end_rotations_at": end_rotations_at,
        }
        response = self._api.post(url, body=data)
        return response.json()


@dataclass
class OnCallEvent(BaseAPIObject):
    """OnCallEvent resource from the BetterStack Uptime API.

    An on-call event represents a time period when specific users
    are on-call.

    Attributes:
        starts_at: Start time of the event in ISO 8601 format.
        ends_at: End time of the event in ISO 8601 format.
        users: List of email addresses of users on-call during this event.
        override: Whether this is an override event.
    """

    type: ClassVar[str] = "on_call_event"
    _url_endpoint: ClassVar[str] = "on-calls/{calendar_id}/events"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page"]

    # Known fields with types
    starts_at: str | None = None
    ends_at: str | None = None
    users: list[str] | None = None
    override: bool | None = None

    # Private fields
    _calendar_id: str | None = field(default=None, repr=False, compare=False)

    def generate_url(self) -> str:
        """Create the URL for this event endpoint.

        Returns:
            Full event URL path.

        Raises:
            ValueError: If calendar_id is not set.
        """
        if self._calendar_id is None:
            raise ValueError("calendar_id is required to generate URL")
        return f"on-calls/{self._calendar_id}/events/{self.id}"

    @classmethod
    def generate_global_url(cls) -> str:
        """Events don't have a global URL without a calendar ID.

        Raises:
            ValueError: Always, as events require a calendar ID.
        """
        raise ValueError("OnCallEvent requires a calendar_id to generate URL")
