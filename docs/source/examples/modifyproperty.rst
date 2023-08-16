Modify Property
---------------

.. highlight:: python
.. code-block:: python
    
    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Monitor

    api = UptimeAPI("yourtokenhere")
    monitor = Monitor(api=api, id=1234)

    monitor.paused = True
    monitor.save()