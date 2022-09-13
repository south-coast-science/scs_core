"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserFinder(object):
    """
    classdocs
    """

    __URL = 'https://iw0jza59y1.execute-api.us-west-2.amazonaws.com/default/CognitoUsersFinder/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                    # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        url = '/'.join((self.__URL, 'all'))

        response = self.__http_client.get(url, headers=self.__headers(token))
        self.__check_response(response)

        # print("response: %s" % response.json())

        return (CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_status(self, token, confirmation_status):
        url = '/'.join((self.__URL, confirmation_status.lower()))

        response = self.__http_client.get(url, headers=self.__headers(token))
        self.__check_response(response)

        return (CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_enabled(self, token, enabled):
        url = '/'.join((self.__URL, 'enabled' if enabled else 'disabled'))

        response = self.__http_client.get(url, headers=self.__headers(token))
        self.__check_response(response)

        return (CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_email(self, token, email):
        url = '/'.join((self.__URL, 'in'))
        payload = JSONify.dumps({"Email": email})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return (CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_usernames(self, token, usernames):
        url = '/'.join((self.__URL, 'usernames'))
        payload = JSONify.dumps(usernames)

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return (CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def get_by_email(self, token, email):
        url = '/'.join((self.__URL, 'exact'))
        payload = JSONify.dumps({"Email": email})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    def get_self(self, token):
        url = '/'.join((self.__URL, 'self'))

        response = self.__http_client.get(url, headers=self.__headers(token))
        self.__check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __headers(self, token):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Token": token}
        self.__logger.debug('headers: %s' % headers)

        return headers


    def __check_response(self, response):
        self.__logger.debug('response: %s' % response.json())

        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserFinder:{http_client:%s}" % self.__http_client
