"""
Created on 17 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint

from scs_core.control.control_receipt import ControlReceipt

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('DevCtrlAPI/DeviceControl',
                   'https://4fq7dy8f15.execute-api.us-west-2.amazonaws.com/default/DeviceControl')


# --------------------------------------------------------------------------------------------------------------------

class DeviceControlClient(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def interact(self, token, device_tag, cmd_tokens):
        payload = {
            'device-tag': device_tag,
            'message': [str(token) for token in cmd_tokens]
        }

        response = requests.post(Endpoint.url(), headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        return ControlReceipt.construct_from_jdict(json.loads(response.json()))
