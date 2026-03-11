Exceptions
==========

The library provides a hierarchy of exceptions for handling API errors gracefully.

Exception Hierarchy
-------------------

.. code-block:: text

    BetterStackError (base)
    ├── APIError
    │   ├── AuthenticationError (401)
    │   ├── ForbiddenError (403)
    │   ├── NotFoundError (404)
    │   ├── RateLimitError (429)
    │   └── ServerError (5xx)
    ├── ValidationError
    └── ConfigurationError

Usage Example
-------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor
    from betterstack.uptime.exceptions import (
        AuthenticationError,
        NotFoundError,
        RateLimitError,
        APIError,
    )

    api = UptimeAPI("your-token")

    try:
        monitor = Monitor.get_all_instances(api)
    except AuthenticationError:
        print("Invalid API token")
    except NotFoundError:
        print("Resource not found")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
    except APIError as e:
        print(f"API error {e.status_code}: {e.message}")

Exception Reference
-------------------

BetterStackError
^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.BetterStackError
   :members:
   :show-inheritance:

APIError
^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.APIError
   :members:
   :show-inheritance:

AuthenticationError
^^^^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.AuthenticationError
   :members:
   :show-inheritance:

ForbiddenError
^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.ForbiddenError
   :members:
   :show-inheritance:

NotFoundError
^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.NotFoundError
   :members:
   :show-inheritance:

RateLimitError
^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.RateLimitError
   :members:
   :show-inheritance:

ServerError
^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.ServerError
   :members:
   :show-inheritance:

ValidationError
^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.ValidationError
   :members:
   :show-inheritance:

ConfigurationError
^^^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.exceptions.ConfigurationError
   :members:
   :show-inheritance:
