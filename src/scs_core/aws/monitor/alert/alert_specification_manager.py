"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.monitor.alert.alert_specification_intercourse import AlertSpecificationFindRequest, \
    AlertSpecificationFindResponse

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class AlertSpecificationManager(APIClient):
    """
    classdocs
    """

    __URL = "https://a066wbide8.execute-api.us-west-2.amazonaws.com/default/AlertSpecification"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, description_filter, topic_filter, path_filter, creator_filter):
        request = AlertSpecificationFindRequest(description_filter, topic_filter, path_filter, creator_filter)

        response = requests.get(self.__URL, headers=self._token_headers(token), params=request.params())
        self._check_response(response)

        return AlertSpecificationFindResponse.construct_from_jdict(response.json())


    def retrieve(self, token, id):
        url = '/'.join((self.__URL, str(id)))

        http_response = requests.get(url, headers=self._token_headers(token))
        self._check_response(http_response)

        response = AlertSpecificationFindResponse.construct_from_jdict(http_response.json())

        return response.alerts[0] if response.alerts else None


    def create(self, token, alert):
        http_response = requests.post(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(alert))
        self._check_response(http_response)

        response = AlertSpecificationFindResponse.construct_from_jdict(http_response.json())

        return response.alerts[0] if response.alerts else None


    def update(self, token, alert):
        url = '/'.join((self.__URL, str(alert.id)))

        http_response = requests.post(url, headers=self._token_headers(token), data=JSONify.dumps(alert))
        self._check_response(http_response)

        response = AlertSpecificationFindResponse.construct_from_jdict(http_response.json())

        return response.alerts[0] if response.alerts else None


    def delete(self, token, id):
        url = '/'.join((self.__URL, str(id)))

        http_response = requests.delete(url, headers=self._token_headers(token))
        self._check_response(http_response)
