Working with Monitors
=====================

Get All Monitors
----------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    for monitor in Monitor.get_all_instances(api):
        print(f"{monitor.url}: {monitor.status}")

Create a New Monitor
--------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    monitor = Monitor.new(
        api,
        url="https://example.com",
        monitor_type="status",
        check_frequency=30,
        regions=["us", "eu"],
    )

    print(f"Created monitor with ID: {monitor.id}")

Update a Monitor
----------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    # Get an existing monitor
    for monitor in Monitor.get_all_instances(api):
        if monitor.url == "https://example.com":
            # Modify properties
            monitor.paused = True
            monitor.check_frequency = 60

            # Save changes (only modified fields are sent)
            monitor.save()
            break

Get or Create
-------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    # Get existing or create new
    created, monitor = Monitor.get_or_create(
        api,
        url="https://example.com",
    )

    if created:
        print("New monitor created")
    else:
        print("Found existing monitor")

Get Monitor SLA Data
--------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    for monitor in Monitor.get_all_instances(api):
        # Access SLA data (lazy-loaded)
        sla = monitor.sla

        print(f"{monitor.url}:")
        print(f"  Availability: {sla.availability}%")
        print(f"  Total downtime: {sla.downtime_duration}s")
        print(f"  Incidents: {sla.number_of_incidents}")

        # Change timeframe for SLA calculation
        sla.timeframe = ("2024-01-01", "2024-12-31")
        print(f"  Yearly availability: {sla.availability}%")

Working with Monitor Groups
---------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import MonitorGroup

    api = UptimeAPI("your-token")

    for group in MonitorGroup.get_all_instances(api):
        print(f"Group: {group.name}")

        # Get monitors in this group (lazy-loaded)
        for monitor in group.monitors:
            print(f"  - {monitor.url}")
