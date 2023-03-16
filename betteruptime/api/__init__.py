import requests
import json
from urllib.parse import urljoin, urlparse, parse_qs
from .auth import BearerAuth
from .mixins import DynamicVariableMixin


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

    # Pretty obvious, don't you think?
    def get(self, url, body=None, headers=None, parameters=None):
        r = requests.get(url=urljoin(self.base_url, url), params=parameters, headers=headers, auth=self.auth)
        return r.json()
    def post(self, url, body=None, headers=None, parameters=None):
        r = requests.post(url=urljoin(self.base_url, url), json=body, params=parameters, headers=headers, auth=self.auth)
        return r
    def patch(self, url, body=None, headers=None, parameters=None):
        r = requests.patch(url=urljoin(self.base_url, url), json=body, params=parameters, headers=headers, auth=self.auth)
        return r
    def delete(self, url, body):
        return requests.delete(url=urljoin(self.base_url, url), auth=self.auth)


class PaginatedAPI(RESTAPI):
    '''
    Specically used with paginated API views
    '''
    def get(self, url, body=None, headers=None, parameters={}):
        '''
        Overrides the default behaviour, and checks for the pagination.next field.
        If it's there: follow it (and it's parameters) untill it's empty.
        '''
        data=super().get(url, body, headers, parameters)
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

class BetterUptimeAPI(PaginatedAPI):
    def __init__(self, bearer_token):
        super().__init__("https://betteruptime.com/api/v2/", BearerAuth(bearer_token))


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
