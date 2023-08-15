import requests


class BearerAuth(requests.auth.AuthBase):
    '''
    Wraps the authorization for requests in order to use BearerAuth easily
    '''
    def __init__(self, token: str):
        '''
        Initialize BearerAuth using token

        :param str token: Token to be used
        '''

        self.token = token

    def __call__(self, r: requests.Request):
        '''
        Overrides the __call__ function in order to modify request header

        :param Request r: Request object to modify
        :return: Modified Request object
        :rtype: Request
        '''

        r.headers["authorization"] = "Bearer %s" % self.token
        return r
