betterstack.uptime package
==========================

Examples
--------

Print all monitor URLs
^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: python
.. code-block:: python

   from betterstack.uptime import UptimeAPI
   from betterstack.uptime.objects import Montitor

   api = UptimeAPI("yourtokenhere")
   monitors = Monitor.get_all_instances(api)

   for monitor in monitors:
      print(monitor.url)


Change variable for specific monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: python
.. code-block:: python

   from betterstack.uptime import UptimeAPI
   from betterstack.uptime.objects import Montitor

   api = UptimeAPI("yourtokenhere")
   monitor = Monitor(api=api, id=1234)
   monitor.regions = ['eu']
   monitor.save()

Get Monitor SLA for time period
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: python
.. code-block:: python

   from betterstack.uptime import UptimeAPI
   from betterstack.uptime.objects import Montitor

   start_date = "2023-07-14"
   end_date = "2023-08-14"

   api = UptimeAPI("yourtokenhere")
   monitor = Monitor(api=api, id=1234)
   monitor._sla.timeframe = (start_date, end_date)

   print(monitor._sla.availablilty)
   print(monitor._sla.total_downtime)
   print(monitor._sla.number_of_incidents)

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   betterstack.uptime.auth
   betterstack.uptime.helpers
   betterstack.uptime.mixins
   betterstack.uptime.objects


Module contents
---------------

.. automodule:: betterstack.uptime
   :members:
   :undoc-members:
   :show-inheritance:


