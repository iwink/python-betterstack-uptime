"""Heartbeat Group API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    from .heartbeat import Heartbeat


@dataclass
class HeartbeatGroup(BaseAPIObject):
    """Heartbeat Group resource from the BetterStack Uptime API.

    A heartbeat group is a collection of heartbeat monitors that can
    be managed together. Groups help organize heartbeats logically and
    can be paused/resumed as a unit.

    Attributes:
        name: The name of the heartbeat group.
        sort_index: Sort order for the group in the dashboard.
        created_at: When the group was created (ISO 8601 format).
        updated_at: When the group was last updated (ISO 8601 format).
        paused: Whether all heartbeats in the group are paused.
        team_name: The team that owns this heartbeat group (for filtering).
    """

    type: ClassVar[str] = "heartbeat_group"
    _url_endpoint: ClassVar[str] = "heartbeat-groups"
    _allowed_query_parameters: ClassVar[list[str]] = ["team_name"]

    # Known fields
    name: str | None = None
    sort_index: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    paused: bool | None = None
    team_name: str | None = None

    # Private fields
    _heartbeats: list[Heartbeat] | None = field(default=None, repr=False, compare=False)

    @property
    def heartbeats(self) -> list[Heartbeat]:
        """Get heartbeats in this group, fetching if necessary.

        Returns:
            List of Heartbeat objects in this group.
        """
        if self._heartbeats is None:
            self.fetch_heartbeats()
        return self._heartbeats or []

    def fetch_heartbeats(self) -> None:
        """Fetch all heartbeats belonging to this group."""
        if self._api is None:
            raise ValueError("API not set")
        from .heartbeat import Heartbeat

        data = self._api.get(f"{self.generate_url()}/heartbeats")
        self._heartbeats = []
        for item in data:
            self._heartbeats.append(Heartbeat._from_api_response(self._api, item))
