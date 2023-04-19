"""
Created on 17 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.client.api_client import APIClient
from scs_core.control.control_receipt import ControlReceipt
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class DeviceControlClient(APIClient):
    """
    classdocs
    """

    __URL = "https://4fq7dy8f15.execute-api.us-west-2.amazonaws.com/default/DeviceControl"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def interact(self, token, device_tag, cmd_tokens):
        payload = {
            'device-tag': device_tag,
            'message': [str(token) for token in cmd_tokens]
        }

        response = self._http_client.post(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        return ControlReceipt.construct_from_jdict(json.loads(response.json()))
