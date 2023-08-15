Delete incident when condition is met
-------------------------------------

.. highlight:: python
.. code-block:: python
    
    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import Incident

    api = UptimeAPI("yourtokenhere")
    incidents = Incident.get_all_instances(api=api)

    for incident in incidents:
        if "SSL" in incident.cause and "expire soon" in incident.cause:
            print("Almost expired SSL cert, %s %s" % (incident.started_at, incident.resolved_at), ", deleting")
            incident.delete()
        if hasattr(incident, "response_options") and incident.response_options and "someheader: someoption" in incident.response_options:
            print("Deleting %s" % incident.name)
            incident.delete()