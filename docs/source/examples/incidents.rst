Working with Incidents
======================

Get All Incidents
-----------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        print(f"Incident: {incident.name}")
        print(f"  Started: {incident.started_at}")
        print(f"  Cause: {incident.cause}")
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

Delete Incidents by Condition
-----------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("your-token")

    for incident in Incident.get_all_instances(api):
        # Delete SSL expiry warnings
        if "SSL" in incident.cause and "expire soon" in incident.cause:
            print(f"Deleting SSL warning: {incident.name}")
            incident.delete()

        # Delete incidents with specific response headers
        if hasattr(incident, "response_options") and incident.response_options:
            if "someheader: someoption" in incident.response_options:
                print(f"Deleting: {incident.name}")
                incident.delete()
