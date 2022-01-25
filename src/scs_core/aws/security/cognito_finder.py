"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.aws.security.cognito_user import CognitoUserIdentity
from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class CognitoFinder(object):
    """
    classdocs
    """

    __URL = 'https://unnyezcdaa.execute-api.us-west-2.amazonaws.com/default/CognitoFinder'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self):
        url = '/'.join((self.__URL, 'all'))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def find_by_status(self, confirmation_status):
        url = '/'.join((self.__URL, confirmation_status.lower()))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def find_by_enabled(self, enabled):
        url = '/'.join((self.__URL, 'enabled' if enabled else 'disabled'))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)
        status = HTTPStatus(response.status_code)

        # print("status_code: %s" % response.status_code)
        # print("text: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def find_by_email(self, email):             # partial match with email
        url = '/'.join((self.__URL, email))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def get_self(self):
        url = '/'.join((self.__URL, 'self'))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        return CognitoUserIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoFinder:{id_token:%s}" % self.__id_token
