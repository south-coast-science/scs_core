"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.monitor.alert.alert_status_intercourse import AlertStatusFindRequest, AlertStatusFindResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('AlertStatAPI/AlertStatus',
                   'https://n0ctatmvjl.execute-api.us-west-2.amazonaws.com/default/AlertStatus')


# --------------------------------------------------------------------------------------------------------------------

class AlertStatusManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, id_filter, cause_filter, response_mode):
        request = AlertStatusFindRequest(id_filter, cause_filter, response_mode)

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=request.params())
        self._check_response(response)

        return AlertStatusFindResponse.construct_from_jdict(response.json())


    def delete(self, token, id):
        url = Endpoint.url(id)

        http_response = requests.delete(url, headers=self._token_headers(token))
        self._check_response(http_response)
