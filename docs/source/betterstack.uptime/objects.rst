API Objects Reference
=====================

This module contains all API resource objects that map to BetterStack Uptime API endpoints.
Each object extends :class:`~betterstack.uptime.base.BaseAPIObject` and provides:

- Automatic attribute mapping from API responses
- Change tracking for efficient updates (only modified fields are sent)
- CRUD operations (create, read, update, delete)
- Class methods for querying and filtering

Monitoring
----------

Monitor
^^^^^^^

.. autoclass:: betterstack.uptime.objects.Monitor
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Monitor SLA
^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.MonitorSLA
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Monitor Groups
^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.MonitorGroup
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Heartbeats
----------

Heartbeat
^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.Heartbeat
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Heartbeat Groups
^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.HeartbeatGroup
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Incidents
---------

.. autoclass:: betterstack.uptime.objects.Incident
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

.. note::
   Incidents use the BetterStack v3 API endpoint (``/api/v3/incidents``) which provides
   additional filtering capabilities and attributes compared to the v2 API.

Status Pages
------------

StatusPage
^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.StatusPage
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

StatusPageSection
^^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.StatusPageSection
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

StatusPageResource
^^^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.StatusPageResource
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

StatusPageGroup
^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.StatusPageGroup
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

On-Call Scheduling
------------------

OnCallCalendar
^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.OnCallCalendar
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

OnCallEvent
^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.OnCallEvent
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

Escalation Policies
-------------------

EscalationPolicy
^^^^^^^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.EscalationPolicy
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: type
   :no-index:

.. note::
   Escalation policies use the BetterStack v3 API endpoint (``/api/v3/policies``).

PolicyStep
^^^^^^^^^^

.. autoclass:: betterstack.uptime.objects.PolicyStep
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. note::
   ``PolicyStep`` is a helper dataclass for constructing policy steps. It is not an API object
   and cannot be used for direct API operations.
