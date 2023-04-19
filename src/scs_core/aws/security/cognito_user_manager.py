"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCreator(APIClient):
    """
    classdocs
    """

    __URL = 'https://0knr39qhv7.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccountCreator'
    __AUTH = '@southcoastscience.com'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = self._auth_headers(self.__AUTH)

        response = self._http_client.post(self.__URL, headers=headers, json=identity.as_json())
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserEditor(APIClient):
    """
    classdocs
    """

    __URL = 'https://fru3uy2z82.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccounts/edit'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, token):
        super().__init__(http_client)

        self.__token = token                            # string


    # ----------------------------------------------------------------------------------------------------------------

    def update(self, identity):
        headers = self._token_headers(self.__token)

        response = self._http_client.patch(self.__URL, headers=headers, data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserEditor:{token:%s}" % self.__token


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserDeleter(APIClient):
    """
    classdocs
    """

    __URL = 'https://fru3uy2z82.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccounts/delete/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, token):
        super().__init__(http_client)

        self.__token = token                            # string


    # ----------------------------------------------------------------------------------------------------------------

    def delete(self, email):
        url = '/'.join((self.__URL, email))
        headers = self._token_headers(self.__token)

        response = self._http_client.delete(url, headers=headers)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserDeleter:{token:%s}" % self.__token
