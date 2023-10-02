"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.monitor.device.device_monitor_report import DeviceMonitorReport


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorStatusManager(APIClient):
    """
    classdocs
    """

    __URL = "https://0l7fwqkzr8.execute-api.us-west-2.amazonaws.com/default/DeviceMonitorStatus"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, device_tag_filter=None, exact=False):
        payload = {
            'device_tag': device_tag_filter,
            'exact': exact
        }

        response = requests.get(self.__URL, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return DeviceMonitorReport.construct_from_jdict(response.json())
