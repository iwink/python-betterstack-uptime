API Client
==========

The API client classes handle all HTTP communication with the BetterStack Uptime API.

Quick Start
-----------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    # Initialize the client with your API token
    api = UptimeAPI("your-bearer-token")

    # Get all monitors
    for monitor in Monitor.get_all_instances(api):
        print(f"{monitor.url}: {monitor.status}")

UptimeAPI
---------

The main client class for interacting with the BetterStack Uptime API.

.. autoclass:: betterstack.uptime.api.UptimeAPI
   :members:
   :undoc-members:
   :show-inheritance:

PaginatedAPI
------------

Base class that handles automatic pagination of API responses.

.. autoclass:: betterstack.uptime.api.PaginatedAPI
   :members:
   :undoc-members:
   :show-inheritance:

RESTAPI
-------

Low-level REST API client with retry logic and error handling.

.. autoclass:: betterstack.uptime.api.RESTAPI
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Options
---------------------

The ``UptimeAPI`` client accepts several configuration options:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``bearer_token``
     - (required)
     - Your BetterStack API token
   * - ``retries``
     - 3
     - Number of retry attempts for failed requests
   * - ``backoff_factor``
     - 0.5
     - Multiplier for exponential backoff between retries
   * - ``timeout``
     - 30.0
     - Request timeout in seconds

Example with custom configuration:

.. code-block:: python

    api = UptimeAPI(
        bearer_token="your-token",
        retries=5,
        backoff_factor=1.0,
        timeout=60.0,
    )
