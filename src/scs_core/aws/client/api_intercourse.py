"""
Created on 19 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

separated from client to remove dependency on requests package
"""

from abc import ABC, abstractmethod
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class APIResponse(JSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # server...

    def as_http(self, status=HTTPStatus.OK):
        response = HTTPResponse(status, self)

        return response.as_http()


    # ----------------------------------------------------------------------------------------------------------------
    # client...

    def start(self):
        return None


    @abstractmethod
    def next_params(self, params):
        pass


    @property
    @abstractmethod
    def next_request(self):
        pass


    @property
    def interval(self):
        return None
