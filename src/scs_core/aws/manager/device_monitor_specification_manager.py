"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.data.device_monitor_specification import DeviceMonitorSpecification, DeviceMonitorSpecificationList


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorSpecificationManager(APIClient):
    """
    classdocs
    """

    __URL = "https://psnunpg4gb.execute-api.us-west-2.amazonaws.com/default/DeviceMonitorSpecification"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, email_address=None, device_tag=None, exact=False):
        payload = {
            'email_address': email_address,
            'device_tag': device_tag,
            'exact': exact
        }

        response = self._http_client.get(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorSpecificationList.construct_from_jdict(response.json())


    def add(self, token, email_address, device_tag):
        payload = {
            'email_address': email_address,
            'device_tag': device_tag
        }

        response = self._http_client.post(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorSpecification.construct_from_jdict(response.json())


    def set_suspended(self, token, device_tag, is_suspended):
        payload = {
            'device_tag': device_tag,
            'is_suspended': is_suspended
        }

        response = self._http_client.patch(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorSpecification.construct_from_jdict(response.json())


    def remove(self, token, email_address, device_tag=None):
        payload = {
            'email_address': email_address,
            'device_tag': device_tag
        }

        response = self._http_client.delete(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorSpecificationList.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorSpecificationManager:{}"
