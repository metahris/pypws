import time
from exceptions import AuthException
import requests


class OAuth2Handler:

    def __init__(self, token_url, client_id, client_secret, scope, grant_type='client_credentials'):
        # add more control
        if not token_url:
            raise AuthException('token url cannot be None')
        if not client_id:
            raise AuthException('client_id cannot be None')
        if not client_secret:
            raise AuthException('client_secret cannot be None')
        if not scope:
            raise AuthException('scope cannot be None')
        self.__token_url = token_url
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type

    def get_access_token(self):
        result = dict()
        response = requests.post(
            self.__token_url,
            data={"grant_type": self.grant_type, "scope": self.scope},
            auth=(self.__client_id, self.__client_secret),
        )
        result['access_token'] = response.json()["access_token"]
        result['expires_at'] = time.time() + response.json()["expires_in"]

        return result
