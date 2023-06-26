"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient

from scs_core.aws.data.device_monitor_report import DeviceMonitorReport


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorStatusManager(APIClient):
    """
    classdocs
    """

    # TODO: update URL
    __URL = "https://n0ctatmvjl.execute-api.us-west-2.amazonaws.com/default/DeviceMonitorStatus"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, device_tag_filter=None, exact=False):
        payload = {
            'device_tag': device_tag_filter,
            'exact': exact
        }

        response = self._http_client.get(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        report = DeviceMonitorReport(response.json())

        return report.device(device_tag_filter) if exact else report


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorStatusManager:{}"
