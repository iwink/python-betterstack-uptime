import requests
import json
from urllib.parse import urljoin, urlparse, parse_qs
from .auth import BearerAuth
from .mixins import DynamicVariableMixin
from .helpers import filter_on_attribute


class RESTAPI():
    '''
    Class that will handle all low-level API calls.
    '''

    def __init__(self, base_url, auth):
        '''
        base_url: The URL to be called, ending in a /
        auth: Authentication class to be used with requests
        '''
        if not base_url.endswith("/"):
            raise ValueError("base_url should end with a /")
        self.base_url = base_url
        self.auth = auth

    def clean_params(self, parameters):
        '''
        Removes the trailing underscore in order to be able to use parameters
        like `from`
        parameters: Dict with parameters
        '''
        result = {}
        if parameters == result or parameters is None:
            return result
        for k, v in parameters.items():
            if k.endswith("_"):
                k = k[:-1]
            result[k] = v
        return result

    # Pretty obvious, don't you think?
    def get(self, url, body=None, headers=None, parameters=None):
        parameters = self.clean_params(parameters)
        r = requests.get(url=urljoin(self.base_url, url), params=parameters, headers=headers, auth=self.auth)
        r.raise_for_status()
        return r.json()
    def post(self, url, body=None, headers=None, parameters=None):
        parameters = self.clean_params(parameters)
        r = requests.post(url=urljoin(self.base_url, url), json=body, params=parameters, headers=headers, auth=self.auth)
        r.raise_for_status()
        r.raise_for_status()
        return r
    def patch(self, url, body=None, headers=None, parameters=None):
        parameters = self.clean_params(parameters)
        r = requests.patch(url=urljoin(self.base_url, url), json=body, params=parameters, headers=headers, auth=self.auth)
        r.raise_for_status()
        return r
    def delete(self, url, body=None, headers=None, parameters=None):
        parameters = self.clean_params(parameters)
        r = requests.delete(url=urljoin(self.base_url, url), auth=self.auth)
        r.raise_for_status()
        return r


class PaginatedAPI(RESTAPI):
    '''
    Specically used with paginated API views
    '''
    def get(self, url, body=None, headers=None, parameters=None):
        '''
        Overrides the default behaviour, and checks for the pagination.next field.
        If it's there: follow it (and it's parameters) untill it's empty.
        '''
        data=super().get(url, body, headers, parameters)
        if not parameters:
            parameters = {}
        # Only recurse lists. No need for single objects
        if isinstance(data['data'], dict):
            yield data['data']
            return

        # Return results of first page before recursing
        for monitor in data['data']:
            yield monitor
        
        while data['pagination']['next']:
            # Parse URL parameters so we can use it in a new request
            parameters.update(parse_qs(urlparse(data['pagination']['next']).query))
            data = super().get(url, body, headers, parameters)
            for monitor in data['data']:
                yield monitor

class UptimeAPI(PaginatedAPI):
    def __init__(self, bearer_token):
        super().__init__("https://uptime.betterstack.com/api/v2/", BearerAuth(bearer_token))


class BaseAPIObject(DynamicVariableMixin):
    '''
    Base class for all API objects. Uses dynamically assignable variables
    from api responses in order to store/filter/update data
    Always use the set_variable() function provided by DynamicVariableMixin
    in order to change or assign a variable. This ensures tracking of 
    changed variables
    '''



    _url_endpoint: str
    def __init__(self, api: RESTAPI, id: int, attributes: dict=None, **kwargs):
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
            self.fetch_data(**kwargs)
        else:
            for k, v in attributes.items():
                self.add_tracked_property(k, v)
            self.reset_variable_tracking()
    
    def generate_url(self):
        '''
        Creates the URL in order to get this specific instance
        '''
        return "%s/%i" % (self._url_endpoint, self.id)
    
    @classmethod
    def generate_global_url(cls):
        '''
        Get the overview page for this object type
        '''
        return cls._url_endpoint
        

    def fetch_data(self, **kwargs):
        '''
        Gets all attributes from the API
        '''
        
        try:
            data = self._api.get(self.generate_url(), parameters=kwargs).__next__()
            for k, v in data['attributes'].items():
                self.add_tracked_property(k, v)
            self.reset_variable_tracking()
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
            for var in self.get_modified_properties():
                data[var] = getattr(self, var)
            r = self._api.patch(self.generate_url(), body=data)
            for k, v in r.json()['data']['attributes'].items():
                setattr(self, k, v)
            self.reset_variable_tracking()

    def delete(self):
        '''
        Deletes the object from the API
        '''
        self._api.delete(url=self.generate_url(), body=None)
        self.setattr
    @classmethod
    def get_or_create(cls, api: RESTAPI, **kwargs):
        '''
        Either, fetch an object using queryable attributes, or
        create a new object using said attributes.
        
        api: API instance
        '''
        try:
            instances=list(cls.filter(api, **kwargs))
        except ValueError:
            instances=list(cls.get_all_instances(api))
            for k, v in kwargs.items():
                instances=filter_on_attribute(instances, k, v)
        if len(instances) > 1:
            raise Exception("Multiple matches on get_or_create, should never happen")
        elif len(instances) is 0:
            return True, cls.new(api, **kwargs)
        else:
            return False, instances[0]

    @classmethod
    def new(cls, api: RESTAPI, **kwargs):
        '''
        Creates a new object using specified kwargs
        '''
        data = api.post(cls.generate_global_url(), body=kwargs)
        return cls(api, data.json()['data']['id'], data.json()['data']['attributes'])

    @classmethod
    def filter(cls, api, **kwargs):
        '''
        Uses url parameters to filter objects. Filter options must be 
        in `_allowed_query_parameters` in order to work
        '''
        cls.filter_query_options(**kwargs)
        data = api.get(cls.generate_global_url(), parameters=kwargs)
        for d in data:
            yield cls(api, d['id'], d['attributes'])
    @classmethod
    def get_all_instances(cls, api: PaginatedAPI, **kwargs):
        '''
        Helper class method in order to create instances of all known instances

        api: API instance
        '''
        for instance_json in api.get(cls.generate_global_url()):
            yield cls(api, instance_json['id'], instance_json['attributes'], **kwargs)

        

    @classmethod
    def filter_query_options(cls, **kwargs):
        '''
        Check if query parameters are allowed for this specific object type
        '''
        if not hasattr(cls, "_allowed_query_parameters"):
            raise NotImplementedError("The _allowed_query_parameters variable should be implemented before trying to filter a class")
        if not cls._allowed_query_parameters:
            raise ValueError("%s cannot and should not be filtered!" % cls.__name__)
        for k in kwargs.keys():
            if k not in cls._allowed_query_parameters:
                raise ValueError("%s is not in the allowed query parameters" % k)
