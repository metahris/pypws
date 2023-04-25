import time
from collections import namedtuple

import requests
from aiohttp import ClientSession
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from auths import OAuth2Handler
from exceptions import AuthException

_HTTPVerbs = namedtuple('_HTTPVerbs', ['GET', 'POST', 'PUT', 'DELETE'])
HTTP_VERBS = _HTTPVerbs('GET', 'POST', 'PUT', 'DELETE')


class BaseAPI:
    """
    Base class for api clients using either OAuth2 or token-based authentication
    """
    BASE_REQUEST_HEADERS = {'accept': 'application/json'}

    def __init__(self, config, env):
        self.env = env
        self.__config = config
        self.__auths = getattr(self.__config, env)
        self.__base_url = self.__config.base_url
        self.__resource_url = self.__base_url
        self.__oauth2_handler = None
        self.__token = None
        self.__token_expires_at = None
        if self.__config.authentication == 'OAuth2':
            self.__oauth2_handler = OAuth2Handler(token_url=self.__auths.token_url,
                                                  client_id=self.__auths.client_id,
                                                  client_secret=self.__auths.client_secret,
                                                  scope=self.__auths.scope,
                                                  grant_type=self.__auths.grant_type
                                                  )
            access_token = self.__oauth2_handler.get_access_token()
            self.__token = access_token['access_token']
            self.__token_expires_at = access_token['expires_at']
        elif self.__config.authentication == 'token_based':
            self.__token = self.__auths.token
        else:
            raise AuthException("authentication type must be OAuth2 or token_based")

    def __get_token(self):

        if self.__config.authentication == 'OAuth2':
            if self.__token_expires_at is not None:
                if time.time() < self.__token_expires_at - 60:
                    return self.__token
            self.__oauth2_handler = OAuth2Handler(token_url=self.__auths.token_url,
                                                  client_id=self.__auths.client_id,
                                                  client_secret=self.__auths.client_secret,
                                                  scope=self.__auths.scope,
                                                  grant_type=self.__auths.grant_type
                                                  )
            access_token = self.__oauth2_handler.get_access_token()
            self.__token = access_token['access_token']
            self.__token_expires_at = access_token['expires_at']
        else:
            self.__token = self.__auths.token
        return self.__token

    def _client_session(self, **kwargs):
        return ClientSession(headers=self.__get_headers(), **kwargs)

    def __get_headers(self):
        headers = BaseAPI.BASE_REQUEST_HEADERS.copy()
        headers.update({'Authorization': f'Bearer {self.__get_token()}'})
        return headers

    def _set_resource_url(self, resource):
        self.__resource_url = f'{self.__base_url}/{resource}'

    def _get(self, endpoint='', data=None, json=None, params=None):
        kwargs = dict(data=data, json=json, params=params)
        return self.__request(HTTP_VERBS.GET, f'{self.__resource_url}/{endpoint}', **kwargs)

    def _post(self, endpoint='', data=None, json=None, params=None):
        kwargs = dict(data=data, json=json, params=params)
        return self.__request(HTTP_VERBS.POST, f'{self.__resource_url}/{endpoint}', **kwargs)

    def _put(self, endpoint='', data=None, json=None, params=None):
        kwargs = dict(data=data, json=json, params=params)
        return self.__request(HTTP_VERBS.PUT, f'{self.__resource_url}/{endpoint}', **kwargs)

    def _delete(self, endpoint='', data=None, json=None, params=None):
        kwargs = dict(data=data, json=json, params=params)
        return self.__request(HTTP_VERBS.DELETE, f'{self.__resource_url}/{endpoint}', **kwargs)

    def __request(self, method, url, params=None, data=None, files=None, json=None, verify=False):
        try:
            kwargs = {
                'method': method,
                'url': url,
                'params': params,
                'data': data,
                'files': files,
                'json': json,
                'headers': self.__get_headers(),
                'verify': verify,
            }
            with requests.Session as session:
                retries = Retry(total=3, backoff_factor=0.2, status_forcelist=[502, 504],
                                method_whitelist=[HTTP_VERBS.POST, HTTP_VERBS.GET])
                adapter = HTTPAdapter(max_retries=retries)
                session.mount('http://', adapter)
                session.hooks['response'] = [BaseAPI.__check_response_status]
                response = session.request(**kwargs)
                total_records = response.headers.get('X-Total-Count')
                data = response.json()
                if total_records:
                    return dict(data=data, total_records=int(total_records))
                return data
        except Exception as exc:
            raise exc

    @staticmethod
    def __check_response_status(response, *args, **kwargs):
        """
        shorthand to check if the response is valid
        pycharm may indicate that the args and kwargs parameters are not used
        But they are used implicitly inside the hook response of session object
        """
        response.raise_for_status()

    async def _get_async(self, session, endpoint, **kwargs):
        options = {
            'params': kwargs.get('params'),
            'json': kwargs.get('json'),
            'data': kwargs.get('data')
        }
        async with session.get(url=f'{self.__resource_url}/{endpoint}', **options) as response:
            return await response.json()

    async def _post_async(self, session, endpoint, **kwargs):
        options = {
            'params': kwargs.get('params'),
            'json': kwargs.get('json'),
            'data': kwargs.get('data')
        }
        async with session.post(url=f'{self.__resource_url}/{endpoint}', **options) as response:
            return await response.json()

    async def _put_async(self, session, endpoint, **kwargs):
        options = {
            'params': kwargs.get('params'),
            'json': kwargs.get('json'),
            'data': kwargs.get('data')
        }
        async with session.put(url=f'{self.__resource_url}/{endpoint}', **options) as response:
            return await response.json()

    async def _delete_async(self, session, endpoint, **kwargs):
        options = {
            'params': kwargs.get('params'),
            'json': kwargs.get('json'),
            'data': kwargs.get('data')
        }
        async with session.delete(url=f'{self.__resource_url}/{endpoint}', **options) as response:
            return await response.json()


