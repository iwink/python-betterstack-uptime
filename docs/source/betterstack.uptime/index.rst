Module betterstack.uptime
=========================

The ``betterstack.uptime`` module provides a Python interface to the BetterStack Uptime API.
It converts API endpoints into Python objects with automatic attribute mapping, change tracking,
and full CRUD support.

Quick Start
-----------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor, Incident

    # Initialize the API client
    api = UptimeAPI("your-bearer-token")

    # Get all monitors
    for monitor in Monitor.get_all_instances(api):
        print(f"{monitor.url}: {monitor.status}")

    # Get incidents for a specific monitor
    for incident in Incident.filter(api, monitor_id=12345):
        print(f"{incident.started_at}: {incident.cause}")

API Response Format
-------------------

The BetterStack API returns data in the following format, which is automatically
parsed and mapped to object attributes:

.. code-block:: json

    {
        "data": {
            "id": "12345",
            "type": "monitor",
            "attributes": {
                "url": "https://example.com",
                "status": "up",
                "check_frequency": 30
            }
        }
    }

Submodules
----------

.. toctree::
    :maxdepth: 2

    api
    base
    objects
    exceptions
    auth
    helpers

Module Contents
---------------

.. automodule:: betterstack.uptime
   :members:
   :undoc-members:
   :show-inheritance:
