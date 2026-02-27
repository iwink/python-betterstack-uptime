Base Classes
============

The base classes provide the foundation for all API resource objects.

BaseAPIObject
-------------

The base class that all API resource objects inherit from. It provides:

- Automatic attribute mapping from API responses
- Change tracking for efficient updates
- CRUD operations (create, read, update, delete)
- Class methods for querying and filtering

.. autoclass:: betterstack.uptime.base.BaseAPIObject
   :members:
   :undoc-members:
   :show-inheritance:

Common Operations
-----------------

All objects inheriting from ``BaseAPIObject`` support these operations:

Fetching All Instances
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("your-token")

    # Returns a generator that handles pagination automatically
    for monitor in Monitor.get_all_instances(api):
        print(monitor.url)

Getting or Creating
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Get existing object or create new one
    created, monitor = Monitor.get_or_create(
        api,
        url="https://example.com",
        monitor_type="status",
    )

    if created:
        print("New monitor created")
    else:
        print("Existing monitor found")

Modifying and Saving
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Only modified fields are sent to the API
    monitor.paused = True
    monitor.check_frequency = 60
    monitor.save()

    # Check what was modified
    print(monitor.get_modified_properties())

Deleting
^^^^^^^^

.. code-block:: python

    monitor.delete()

Filtering
^^^^^^^^^

.. code-block:: python

    # Filter using API query parameters
    incidents = Incident.filter(api, monitor_id=12345)

    for incident in incidents:
        print(incident.cause)
