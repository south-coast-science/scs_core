"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.aws.security.cognito_user import CognitoUserIdentity
from scs_core.data.json import JSONify
from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCreator(object):
    """
    classdocs
    """

    __AUTHORIZATION = '@southcoastscience.com'
    __URL = 'https://0knr39qhv7.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccountCreator'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = {'Authorization': self.__AUTHORIZATION}

        response = self.__http_client.post(self.__URL, headers=headers, json=identity.as_json())
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        return CognitoUserIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCreator:{}"


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserEditor(object):
    """
    classdocs
    """

    __URL = 'https://fru3uy2z82.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccounts/edit'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def update(self, identity):
        headers = {'Token': self.__id_token}

        response = self.__http_client.patch(self.__URL, headers=headers, data=JSONify.dumps(identity))
        status = HTTPStatus(response.status_code)

        # print("status_code: %s" % response.status_code)
        # print("text: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserEditor:{id_token:%s}" % self.__id_token


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserDeleter(object):
    """
    classdocs
    """

    __URL = 'https://fru3uy2z82.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccounts/delete/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def delete(self, email):
        url = '/'.join((self.__URL, email))
        headers = {'Token': self.__id_token}

        response = self.__http_client.delete(url, headers=headers)
        status = HTTPStatus(response.status_code)

        # print("status_code: %s" % response.status_code)
        # print("text: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserDeleter:{id_token:%s}" % self.__id_token
