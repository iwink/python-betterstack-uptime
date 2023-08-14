from . import BaseAPIObject

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
