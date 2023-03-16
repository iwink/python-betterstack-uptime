from . import BaseAPIObject

class Monitor(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type="monitor"
    _url_endpoint="monitors"

class MonitorGroup(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type="monitor_group"
    _url_endpoint="monitor-groups"

class Heartbeat(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type="heartbeat"
    _url_endpoint="heartbeats"
    
class HeartbeatGroup(BaseAPIObject):
    '''
    Subclass in order to differentiate between endpoints and types. Can be used to store custom functionality
    '''
    type="heartbeat-group"
    _url_endpoint="heartbeat-groups"
