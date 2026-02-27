"""BetterStack API client libraries.

This package provides Python interfaces for BetterStack services.

Currently available:
    - uptime: BetterStack Uptime API for monitoring and incident management

Example:
    >>> from betterstack.uptime import UptimeAPI, Monitor
    >>> api = UptimeAPI("your-bearer-token")
    >>> monitors = list(Monitor.get_all_instances(api))
"""

__version__ = "2.0.0"
