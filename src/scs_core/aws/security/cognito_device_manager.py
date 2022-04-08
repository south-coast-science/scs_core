"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.data.json import JSONify
from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCreator(object):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices/add'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = {'Token': self.__id_token}

        response = self.__http_client.post(self.__URL, headers=headers, json=identity.as_json())
        status = HTTPStatus(response.status_code)

        # print("response: %s" % response.json())

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceCreator:{id_token:%s}" % self.__id_token


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceEditor(object):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices/update'

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
        return "CognitoDeviceEditor:{id_token:%s}" % self.__id_token


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceDeleter(object):
    """
    classdocs
    """

    __URL = ''

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
        return "CognitoDeviceDeleter:{id_token:%s}" % self.__id_token
