"""BetterStack Uptime API client library.

This module provides a Python interface for the BetterStack Uptime API.

Example:
    >>> from betterstack.uptime import UptimeAPI, Monitor
    >>> api = UptimeAPI("your-bearer-token")
    >>> monitors = list(Monitor.get_all_instances(api))
    >>> for monitor in monitors:
    ...     print(f"{monitor.pronounceable_name}: {monitor.status}")
"""

from .api import RESTAPI, PaginatedAPI, UptimeAPI
from .auth import BearerAuth
from .base import BaseAPIObject
from .exceptions import (
    APIError,
    AuthenticationError,
    BetterStackError,
    ConfigurationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .helpers import filter_on_attribute
from .objects import (
    EscalationPolicy,
    Heartbeat,
    HeartbeatGroup,
    Incident,
    Monitor,
    MonitorGroup,
    MonitorSLA,
    OnCallCalendar,
    OnCallEvent,
    PolicyStep,
    StatusPage,
    StatusPageGroup,
    StatusPageResource,
    StatusPageSection,
)

__all__ = [
    "RESTAPI",
    "APIError",
    "AuthenticationError",
    "BaseAPIObject",
    "BearerAuth",
    "BetterStackError",
    "ConfigurationError",
    "EscalationPolicy",
    "ForbiddenError",
    "Heartbeat",
    "HeartbeatGroup",
    "Incident",
    "Monitor",
    "MonitorGroup",
    "MonitorSLA",
    "NotFoundError",
    "OnCallCalendar",
    "OnCallEvent",
    "PaginatedAPI",
    "PolicyStep",
    "RateLimitError",
    "ServerError",
    "StatusPage",
    "StatusPageGroup",
    "StatusPageResource",
    "StatusPageSection",
    "UptimeAPI",
    "ValidationError",
    "filter_on_attribute",
]

__version__ = "2.0.0"
