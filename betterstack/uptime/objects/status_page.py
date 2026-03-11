"""StatusPage API objects for BetterStack Uptime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ..base import BaseAPIObject

if TYPE_CHECKING:
    pass


@dataclass
class StatusPage(BaseAPIObject):
    """StatusPage resource from the BetterStack Uptime API.

    A status page displays the current operational status of your services
    and provides a public-facing view for your users.

    Attributes:
        company_name: The name of the company.
        company_url: The URL of the company website.
        contact_url: URL for emergency contact.
        logo_url: URL of the company logo.
        timezone: Timezone for the status page.
        subdomain: Subdomain for the status page (e.g., 'my-company').
        custom_domain: Custom domain for the status page.
        custom_css: Custom CSS for the status page.
        custom_javascript: Custom JavaScript for the status page.
        google_analytics_id: Google Analytics ID for tracking.
        min_incident_length: Minimum incident length in seconds to display.
        announcement: Announcement text to display.
        announcement_embed_visible: Whether the announcement embed is visible.
        announcement_embed_css: Custom CSS for the announcement embed.
        announcement_embed_link: Link for the announcement embed.
        automatic_reports: Whether automatic reports are enabled.
        status_page_group_id: ID of the status page group.
        subscribable: Whether users can subscribe to updates.
        hide_from_search_engines: Whether to hide from search engines.
        password_enabled: Whether password protection is enabled.
        ip_allowlist: List of allowed IP addresses or CIDR ranges.
        history: Number of days to display on the status page.
        aggregate_state: Current aggregate operational state.
        design: Design version ('v1' or 'v2').
        navigation_links: Navigation links for the status page.
        theme: Theme of the status page ('light', 'dark', 'system').
        layout: Layout of the status page ('vertical', 'horizontal').
        created_at: When the status page was created.
        updated_at: When the status page was last updated.
    """

    type: ClassVar[str] = "status_page"
    _url_endpoint: ClassVar[str] = "status-pages"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page"]

    # Known fields with types
    company_name: str | None = None
    company_url: str | None = None
    contact_url: str | None = None
    logo_url: str | None = None
    timezone: str | None = None
    subdomain: str | None = None
    custom_domain: str | None = None
    custom_css: str | None = None
    custom_javascript: str | None = None
    google_analytics_id: str | None = None
    min_incident_length: int | None = None
    announcement: str | None = None
    announcement_embed_visible: bool | None = None
    announcement_embed_css: str | None = None
    announcement_embed_link: str | None = None
    automatic_reports: bool | None = None
    status_page_group_id: int | None = None
    subscribable: bool | None = None
    hide_from_search_engines: bool | None = None
    password_enabled: bool | None = None
    ip_allowlist: list[str] | None = None
    history: int | None = None
    aggregate_state: str | None = None
    design: str | None = None
    navigation_links: list[dict[str, str]] | None = None
    theme: str | None = None
    layout: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    # Private fields for lazy-loaded relationships
    _sections: list[StatusPageSection] | None = field(default=None, repr=False, compare=False)
    _resources: list[StatusPageResource] | None = field(default=None, repr=False, compare=False)

    @property
    def sections(self) -> list[StatusPageSection]:
        """Get the sections for this status page (lazy-loaded).

        Returns:
            List of StatusPageSection objects.
        """
        if self._sections is None:
            self._sections = self.fetch_sections()
        return self._sections

    @property
    def resources(self) -> list[StatusPageResource]:
        """Get the resources for this status page (lazy-loaded).

        Returns:
            List of StatusPageResource objects.
        """
        if self._resources is None:
            self._resources = self.fetch_resources()
        return self._resources

    def fetch_sections(self) -> list[StatusPageSection]:
        """Fetch all sections for this status page from the API.

        Returns:
            List of StatusPageSection objects.
        """
        if self._api is None:
            raise ValueError("API not set")
        url = f"status-pages/{self.id}/sections"
        sections = []
        for item in self._api.get(url):
            section = StatusPageSection._from_api_response(self._api, item)
            section._status_page_id = self.id
            sections.append(section)
        self._sections = sections
        return sections

    def fetch_resources(self) -> list[StatusPageResource]:
        """Fetch all resources for this status page from the API.

        Returns:
            List of StatusPageResource objects.
        """
        if self._api is None:
            raise ValueError("API not set")
        url = f"status-pages/{self.id}/resources"
        resources = []
        for item in self._api.get(url):
            resource = StatusPageResource._from_api_response(self._api, item)
            resource._status_page_id = self.id
            resources.append(resource)
        self._resources = resources
        return resources


@dataclass
class StatusPageSection(BaseAPIObject):
    """StatusPageSection resource from the BetterStack Uptime API.

    A section is a grouping of resources on a status page.

    Attributes:
        name: The name of the section.
        position: The position of the section on the status page.
        created_at: When the section was created.
        updated_at: When the section was last updated.
    """

    type: ClassVar[str] = "status_page_section"
    _url_endpoint: ClassVar[str] = "status-pages/{status_page_id}/sections"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page"]

    # Known fields with types
    name: str | None = None
    position: int | None = None
    created_at: str | None = None
    updated_at: str | None = None

    # Private fields
    _status_page_id: str | None = field(default=None, repr=False, compare=False)

    def generate_url(self) -> str:
        """Create the URL for this section endpoint.

        Returns:
            Full section URL path.

        Raises:
            ValueError: If status_page_id is not set.
        """
        if self._status_page_id is None:
            raise ValueError("status_page_id is required to generate URL")
        return f"status-pages/{self._status_page_id}/sections/{self.id}"

    @classmethod
    def generate_global_url(cls) -> str:
        """Sections don't have a global URL without a status page ID.

        Raises:
            ValueError: Always, as sections require a status page ID.
        """
        raise ValueError("StatusPageSection requires a status_page_id to generate URL")


@dataclass
class StatusPageResource(BaseAPIObject):
    """StatusPageResource resource from the BetterStack Uptime API.

    A resource represents a monitor, heartbeat, or other item displayed
    on a status page.

    Attributes:
        status_page_section_id: ID of the section containing this resource.
        resource_id: ID of the underlying resource (monitor, heartbeat, etc.).
        resource_type: Type of the resource ('Monitor', 'Heartbeat', etc.).
        history: Whether to show history for this resource.
        widget_type: Widget type ('plain', 'history', 'response_times', 'chart_only').
        public_name: Public name displayed on the status page.
        explanation: Help text for the resource.
        position: Position of the resource on the status page.
        fixed_position: Whether position reorders are prevented.
        availability: Availability percentage of the resource.
        status: Current operational status.
        status_history: Historical status data.
    """

    type: ClassVar[str] = "status_page_resource"
    _url_endpoint: ClassVar[str] = "status-pages/{status_page_id}/resources"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page"]

    # Known fields with types
    status_page_section_id: int | None = None
    resource_id: int | None = None
    resource_type: str | None = None
    history: bool | None = None
    widget_type: str | None = None
    public_name: str | None = None
    explanation: str | None = None
    position: int | None = None
    fixed_position: bool | None = None
    availability: float | None = None
    status: str | None = None
    status_history: list[dict[str, Any]] | None = None

    # Private fields
    _status_page_id: str | None = field(default=None, repr=False, compare=False)

    def generate_url(self) -> str:
        """Create the URL for this resource endpoint.

        Returns:
            Full resource URL path.

        Raises:
            ValueError: If status_page_id is not set.
        """
        if self._status_page_id is None:
            raise ValueError("status_page_id is required to generate URL")
        return f"status-pages/{self._status_page_id}/resources/{self.id}"

    @classmethod
    def generate_global_url(cls) -> str:
        """Resources don't have a global URL without a status page ID.

        Raises:
            ValueError: Always, as resources require a status page ID.
        """
        raise ValueError("StatusPageResource requires a status_page_id to generate URL")


@dataclass
class StatusPageGroup(BaseAPIObject):
    """StatusPageGroup resource from the BetterStack Uptime API.

    A status page group is used to organize multiple status pages.

    Attributes:
        name: The name of the group.
        sort_index: Sorting index for the group.
        created_at: When the group was created.
        updated_at: When the group was last updated.
    """

    type: ClassVar[str] = "status_page_group"
    _url_endpoint: ClassVar[str] = "status-page-groups"
    _allowed_query_parameters: ClassVar[list[str]] = ["per_page"]

    # Known fields with types
    name: str | None = None
    sort_index: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
