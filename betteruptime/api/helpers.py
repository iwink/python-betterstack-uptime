from .mixins import DynamicVariableMixin
from . import RESTAPI, PaginatedAPI, BetterUptimeAPI


def filter_on_attribute(objects: list, name: str, value):
    '''
    Used to be able to filter a list of objects on a specific variable

    objects: List of objects
    name: Name of the variable to be checked (str)
    value: Value to be matched
    '''
    return [x for x in objects if getattr(x, name) == value]



class BaseAPIObject(DynamicVariableMixin):
    '''
    Base class for all API objects. Uses dynamically assignable variables
    from api responses in order to store/filter/update data
    Always use the set_variable() function provided by DynamicVariableMixin
    in order to change or assign a variable. This ensures tracking of 
    changed variables
    '''



    _url_endpoint: str
    def __init__(self, api: RESTAPI, id: int, attributes: dict=None):
        '''
        Initializes the object with a corresponding API client, id and optional attributes
        If only the ID is provided, it will fetch data from the API in order to fill it's
        attributes. If attributes are provided, just assign them

        api: API instance
        id: ID used in the API
        attributes: Used for limiting the amount of requests. Dict with all variables needed
        '''
        self._api = api
        if not id or int(id) < 1:
            raise ValueError("Not a valid ID")
        self.id = int(id)
        if not attributes:
            self.fetch_data()
        else:
            for k, v in attributes.items():
                self.set_variable(k, v, noupdate=True)

    def fetch_data(self):
        '''
        Gets all attributes from the API
        '''
        
        try:
            data = self._api.get("%s/%i" % (self._url_endpoint, self.id)).__next__()
            for k, v in data['attributes'].items():
                self.set_variable(k, v, noupdate=True)
        #TODO Better exception handling
        except Exception as e:
            raise e

    def save(self):
        '''
        Update all changed variables inside the class on the API.
        Updated list is provided by DynamicVariableMixin
        '''
        if self._updated_vars:
            data={}
            for var in self._updated_vars:
                data[var] = getattr(self, var)
            r = self._api.patch("%s/%i" % (self._url_endpoint, self.id), body=data)
            for k, v in r.json()['data']['attributes'].items():
                self.set_variable(k, v, noupdate=True)


    @classmethod
    def new(cls, api: RESTAPI, url: str, attributes: dict={}):
        attributes['url'] = url
        data = api.post(cls._url_endpoint, body=attributes)
        return cls(api, data.json()['data']['id'], data.json()['data']['attributes'])

    @classmethod
    def get_all_instances(cls, api: PaginatedAPI):
        '''
        Helper class method in order to create instances of all known instances

        api: API instance
        '''
        instances=[]
        for instance_json in api.get(cls._url_endpoint):
            instances.append(cls(api, instance_json['id'], instance_json['attributes']))
        return instances
