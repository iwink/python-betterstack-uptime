betterstack.uptime package
==========================

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   betterstack.uptime.auth
   betterstack.uptime.helpers
   betterstack.uptime.mixins
   betterstack.uptime.objects

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
   monitor = Monitor(id=1234)
   monitor.regions = ['eu']
   monitor.save()


Module contents
---------------

.. automodule:: betterstack.uptime
   :members:
   :undoc-members:
   :show-inheritance:


