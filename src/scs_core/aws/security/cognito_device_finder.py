"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from http import HTTPStatus

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceFinder(object):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices/retrieve'

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

        return (CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_tag(self, token, tag):
        url = '/'.join((self.__URL, 'in'))
        payload = json.dumps({"username": tag})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return (CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


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
        return "CognitoDeviceFinder:{http_client:%s}" % self.__http_client
