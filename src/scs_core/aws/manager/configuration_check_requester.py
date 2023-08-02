"""
Created on 26 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

import requests

from collections import OrderedDict
from http import HTTPStatus

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.data.http_response import HTTPResponse

from scs_core.client.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequester(APIClient):
    """
    classdocs
    """

    __URL = "https://5nkrlhaq69.execute-api.us-west-2.amazonaws.com/default/MQTTConfigQueuer"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, token, tag):
        params = {'tag': tag}

        response = requests.get(self.__URL, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return ConfigurationCheckRequesterResponse.construct_from_jdict(response.json())


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequesterResponse(HTTPResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        status = HTTPStatus(jdict.get('statusCode'))

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, status.phrase, status.description)

        result = jdict.get('result')

        return cls(status, result)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, result):
        """
        Constructor
        """
        super().__init__(status)

        self.__result = result                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value
        jdict['result'] = self.result

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def result(self):
        return self.__result


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationCheckResponse:{status:%s, result:%s}" %  (self.status, self.result)
