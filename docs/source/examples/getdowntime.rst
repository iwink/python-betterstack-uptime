Get downtime for monitor
------------------------

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