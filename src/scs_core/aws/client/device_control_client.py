"""
Created on 17 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from http import HTTPStatus

from scs_core.control.control_receipt import ControlReceipt

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class DeviceControlClient(object):
    """
    classdocs
    """

    __URL = "https://4fq7dy8f15.execute-api.us-west-2.amazonaws.com/default/DeviceControl"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                    # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def interrogate(self, token, device_tag, message):
        payload = {
            'device-tag': device_tag,
            'message': message
        }

        response = self.__http_client.post(self.__URL, headers=self.__headers(token), data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        return ControlReceipt.construct_from_jdict(json.loads(response.json()))


    # ----------------------------------------------------------------------------------------------------------------

    def __headers(self, token):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Token": token}
        self.__logger.debug('headers: %s' % headers)

        return headers


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserFinder:{}"
