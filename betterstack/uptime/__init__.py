"""BetterStack Uptime API client library.

This module provides a Python interface for the BetterStack Uptime API.

Example:
    >>> from betterstack.uptime import UptimeAPI, Monitor
    >>> api = UptimeAPI("your-bearer-token")
    >>> monitors = list(Monitor.get_all_instances(api))
    >>> for monitor in monitors:
    ...     print(f"{monitor.pronounceable_name}: {monitor.status}")
"""

# API client classes
from .api import PaginatedAPI, RESTAPI, UptimeAPI

# Authentication
from .auth import BearerAuth

# Base class
from .base import BaseAPIObject

# Exceptions
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

# Helper utilities
from .helpers import filter_on_attribute

# API objects
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
    # API clients
    "RESTAPI",
    "PaginatedAPI",
    "UptimeAPI",
    # Authentication
    "BearerAuth",
    # Base class
    "BaseAPIObject",
    # Exceptions
    "APIError",
    "AuthenticationError",
    "BetterStackError",
    "ConfigurationError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    # Helpers
    "filter_on_attribute",
    # Objects
    "EscalationPolicy",
    "Heartbeat",
    "HeartbeatGroup",
    "Incident",
    "Monitor",
    "MonitorGroup",
    "MonitorSLA",
    "OnCallCalendar",
    "OnCallEvent",
    "PolicyStep",
    "StatusPage",
    "StatusPageGroup",
    "StatusPageResource",
    "StatusPageSection",
]

__version__ = "2.0.0"
