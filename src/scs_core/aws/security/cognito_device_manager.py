"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceManager(object):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = {'Token': self.__id_token}

        response = self.__http_client.post(self.__URL, headers=headers, data=JSONify.dumps(identity))
        status = HTTPStatus(response.status_code)

        self.__logger.debug("create: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    def update(self, identity):
        headers = {'Token': self.__id_token}

        response = self.__http_client.patch(self.__URL, headers=headers, data=JSONify.dumps(identity))
        status = HTTPStatus(response.status_code)

        self.__logger.debug("update: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def delete(self, device_tag):
        headers = {'Token': self.__id_token}
        payload = {"DeviceTag": device_tag}

        response = self.__http_client.delete(self.__URL, headers=headers, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        self.__logger.debug("delete: %s" % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        # TODO: delete device from organisations


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceManager:{id_token:%s}" % self.__id_token
