"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod
from collections import OrderedDict

from scs_core.aws.data.http_response import HTTPResponse


# --------------------------------------------------------------------------------------------------------------------

class CognitoLoginManager(object):
    """
    classdocs
    """

    __AUTHORIZATION = 'southcoastscience.com'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package


    # ----------------------------------------------------------------------------------------------------------------

    def login(self, credentials):
        headers = {'Authorization': self.__AUTHORIZATION}
        response = self.__http_client.post(self.url, headers=headers, json=credentials.as_json())

        return CognitoAuthenticationResult.construct_from_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def url(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{http_client:%s}" % self.__http_client


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserLoginManager(CognitoLoginManager):
    """
    classdocs
    """

    __URL = 'https://ywmuri8c41.execute-api.us-west-2.amazonaws.com/default/CognitoUserLogin'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def url(self):
        return self.__URL


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceLoginManager(CognitoLoginManager):
    """
    classdocs
    """

    __URL = 'https://xatuk2wgb9.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceLogin'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def url(self):
        return self.__URL


# --------------------------------------------------------------------------------------------------------------------

class CognitoAuthenticationResult(HTTPResponse):
    """
    {"AccessToken": "...",
    "ExpiresIn": 3600,
    "TokenType": "Bearer",
    "RefreshToken": "...",
    "IdToken": "..."}
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_response_jdict(cls, status, jdict):
        if not jdict:
            return None

        result = jdict.get('AuthenticationResult')

        if not result:
            return None

        access_token = result.get('AccessToken')
        expires_in = result.get('ExpiresIn')
        token_type = result.get('TokenType')
        refresh_token = result.get('RefreshToken')
        id_token = result.get('IdToken')

        return cls(status, access_token, expires_in, token_type, refresh_token, id_token)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, access_token, expires_in, token_type, refresh_token, id_token):
        """
        Constructor
        """
        super().__init__(status)

        self.__access_token = access_token                      # string
        self.__expires_in = int(expires_in)                     # int
        self.__token_type = token_type                          # string
        self.__refresh_token = refresh_token                    # string
        self.__id_token = id_token                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['AccessToken'] = self.access_token
        jdict['ExpiresIn'] = self.expires_in
        jdict['TokenType'] = self.token_type
        jdict['RefreshToken'] = self.refresh_token
        jdict['IdToken'] = self.id_token

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def access_token(self):
        return self.__access_token


    @property
    def expires_in(self):
        return self.__expires_in


    @property
    def token_type(self):
        return self.__token_type


    @property
    def refresh_token(self):
        return self.__refresh_token


    @property
    def id_token(self):
        return self.__id_token


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AuthenticationResult:{status:%s, access_token:%s, expires_in:%s, token_type:%s, " \
               "refresh_token:%s, id_token:%s}" % \
               (self.status, self.access_token, self.expires_in, self.token_type,
                self.refresh_token, self.id_token)
