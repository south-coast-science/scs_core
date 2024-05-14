"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint

from scs_core.aws.monitor.device.device_monitor_specification import DeviceMonitorSpecification, \
    DeviceMonitorSpecificationList

from scs_core.data.json import JSONify

from scs_core.email.email import EmailRecipient


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('DevMonSpecAPI/DeviceMonitorSpecification',
                   'https://psnunpg4gb.execute-api.us-west-2.amazonaws.com/default/DeviceMonitorSpecification')


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorSpecificationManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, email_address=None, device_tag=None, exact=False):
        params = {
            'email_address': email_address,
            'device_tag': device_tag,
            'exact': exact
        }

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        return DeviceMonitorSpecificationList.construct_from_jdict(response.json())


    def add(self, token, device_tag, recipient: EmailRecipient):
        payload = {
            'device_tag': device_tag,
            'recipient': recipient
        }

        response = requests.post(Endpoint.url(), headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        return DeviceMonitorSpecification.construct_from_jdict(response.json())


    def set_suspended(self, token, device_tag, is_suspended):
        payload = {
            'device_tag': device_tag,
            'is_suspended': is_suspended
        }

        response = requests.patch(Endpoint.url(), headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorSpecification.construct_from_jdict(response.json())


    def remove(self, token, email_address, device_tag=None):
        params = {
            'email_address': email_address,
            'device_tag': device_tag
        }

        response = requests.delete(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        return DeviceMonitorSpecificationList.construct_from_jdict(response.json())
