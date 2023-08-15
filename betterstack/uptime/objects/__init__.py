from betterstack.uptime import BaseAPIObject, RESTAPI


class Monitor(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "monitor"
    _url_endpoint = "monitors"
    _sla = None
    _sla_from, _sla_to = (None, None)
    _allowed_query_parameters = [
        "url",
        "pronounceable_name",
        "per_page"
    ]

    def __init__(self, api: RESTAPI, id: int, attributes: dict = None, **kwargs):
        super().__init__(api, id, attributes, **kwargs)
        self._sla = MonitorSLA(api, id, **kwargs)


class MonitorSLA(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "monitor_sla"
    _url_endpoint = "monitors/%i/sla"
    _sla_start = None
    _sla_end = None
    _allowed_query_parameters = [
        'from',
        'to'
    ]

    def __init__(self, api: RESTAPI, id: int, sla_from=None, sla_to=None, attributes: dict = None, force_update=False):
        if force_update or (sla_from and sla_to):
            super().__init__(api, id, from_=sla_from, to=sla_to, attributes=attributes)
        else:
            self.id = int(id)
            self._api = api
        self._sla_start = sla_from
        self._sla_end = sla_to

    @property
    def timeframe(self):
        return (self._sla_start, self._sla_end)

    @timeframe.setter
    def timeframe(self, frame):
        start, end = frame
        self._sla_start = start
        self._sla_end = end
        self.fetch_data(from_=start, to=end)

    def generate_url(self):
        return self._url_endpoint % self.id

    @classmethod
    def generate_global_url(cls):
        raise ValueError("No overview available for SLA objects")


class MonitorGroup(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "monitor_group"
    _url_endpoint = "monitor-groups"
    _monitors = None

    _allowed_query_parameters = []

    def __init__(self, api: RESTAPI, id: int, attributes: dict = None):
        super().__init__(api, id, attributes)
        self.fetch_monitors()

    def fetch_monitors(self):
        data = self._api.get("%s/monitors" % self.generate_url())
        self._monitors = []
        for instance in data:
            self._monitors.append(Monitor(self._api, instance['id'], instance['attributes']))


class Heartbeat(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "heartbeat"
    _url_endpoint = "heartbeats"

    _allowed_query_parameters = []


class HeartbeatGroup(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "heartbeat-group"
    _url_endpoint = "heartbeat-groups"


class Incident(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type = "incident"
    _url_endpoint = "incidents"
