"""Monitor Group API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    from .monitor import Monitor


@dataclass
class MonitorGroup(BaseAPIObject):
    """Monitor Group resource from the BetterStack Uptime API.

    A monitor group is a collection of monitors that can be managed together.
    Groups help organize monitors logically and can be paused/resumed as a unit.

    Attributes:
        name: The name of the monitor group.
        sort_index: Sort order for the group in the dashboard.
        created_at: When the group was created (ISO 8601 format).
        updated_at: When the group was last updated (ISO 8601 format).
        paused: Whether all monitors in the group are paused.
        team_name: The team that owns this monitor group (for filtering).
    """

    type: ClassVar[str] = "monitor_group"
    _url_endpoint: ClassVar[str] = "monitor-groups"
    _allowed_query_parameters: ClassVar[list[str]] = ["team_name"]

    # Known fields
    name: str | None = None
    sort_index: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    paused: bool | None = None
    team_name: str | None = None

    # Private fields
    _monitors: list[Monitor] | None = field(default=None, repr=False, compare=False)

    @property
    def monitors(self) -> list[Monitor]:
        """Get monitors in this group, fetching if necessary.

        Returns:
            List of Monitor objects in this group.
        """
        if self._monitors is None:
            self.fetch_monitors()
        return self._monitors or []

    def fetch_monitors(self) -> None:
        """Fetch all monitors belonging to this group."""
        from .monitor import Monitor

        data = self._api.get(f"{self.generate_url()}/monitors")
        self._monitors = []
        for item in data:
            self._monitors.append(Monitor._from_api_response(self._api, item))
