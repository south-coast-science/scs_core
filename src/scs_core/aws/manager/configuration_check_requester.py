"""
Created on 26 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

from collections import OrderedDict
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse
from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequester(object):
    """
    classdocs
    """

    __URL = "https://5nkrlhaq69.execute-api.us-west-2.amazonaws.com/default/MQTTConfigQueuer"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        self.__http_client = http_client                # requests package
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, tag):
        params = {'tag': tag}
        headers = {'Authorization': self.__auth.email_address}

        response = self.__http_client.get(self.__URL, headers=headers, params=params)

        return ConfigurationCheckRequesterResponse.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationCheckRequester:{auth:%s}" % self.__auth


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
