Working with Incidents
======================

.. note::
   Incidents use the v3 API endpoint which provides enhanced filtering and additional
   attributes compared to the v2 API.

Get All Incidents
-----------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        print(f"Incident: {incident.name}")
        print(f"  Status: {incident.status}")
        print(f"  Started: {incident.started_at}")
        print(f"  Cause: {incident.cause}")
        print(f"  Regions: {incident.regions}")
        print(f"  Resolved: {incident.is_resolved}")

Filter Incidents by Monitor
---------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    # Filter by monitor ID
    for incident in Incident.filter(api, monitor_id=12345):
        print(f"{incident.started_at}: {incident.cause}")

Filter Incidents by Time Range
------------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    # Get incidents from a specific time range
    for incident in Incident.filter(
        api,
        from_="2024-01-01",
        to="2024-01-31"
    ):
        print(f"{incident.name}: {incident.status}")

Filter by Resolution Status
---------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    # Get only unresolved incidents
    for incident in Incident.filter(api, resolved=False):
        print(f"Active incident: {incident.name}")

    # Get only acknowledged but unresolved incidents
    for incident in Incident.filter(api, acknowledged=True, resolved=False):
        print(f"In progress: {incident.name}")

Filter by Team
--------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    # Get incidents for a specific team
    for incident in Incident.filter(api, team_name="Production Team"):
        print(f"{incident.name}: {incident.cause}")

Acknowledge an Incident
-----------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        if not incident.is_acknowledged:
            incident.acknowledge(acknowledged_by="John Doe")
            print(f"Acknowledged incident: {incident.name}")

Resolve an Incident
-------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        if not incident.is_resolved:
            incident.resolve(resolved_by="Jane Doe")
            print(f"Resolved incident: {incident.name}")

Working with Incident Metadata
------------------------------

Incidents from the v3 API include metadata about notifications sent:

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        notifications = []
        if incident.call:
            notifications.append("phone call")
        if incident.sms:
            notifications.append("SMS")
        if incident.email:
            notifications.append("email")
        if incident.push:
            notifications.append("push notification")
        if incident.critical_alert:
            notifications.append("critical alert")

        if notifications:
            print(f"{incident.name}: Notified via {', '.join(notifications)}")

Delete Incidents by Condition
-----------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        # Delete SSL expiry warnings
        if "SSL" in (incident.cause or "") and "expire soon" in (incident.cause or ""):
            print(f"Deleting SSL warning: {incident.name}")
            incident.delete()
