"""
Created on 19 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

separated from client to remove dependency on requests package
"""

from abc import ABC, abstractmethod
from http import HTTPStatus

from scs_core.data.json import JSONable, JSONify


# --------------------------------------------------------------------------------------------------------------------

class APIResponse(ABC, JSONable):
    """
    classdocs
    """

    __CORS_HEADERS = {                                      # Cross-Origin Resource Sharing
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True
    }

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # server...

    def as_http(self, status=HTTPStatus.OK, cors=False):
        jdict = {
            'statusCode': int(status),
            'body': JSONify.dumps(self)
        }

        if cors:
            jdict['headers'] = self.__CORS_HEADERS

        return jdict


    # ----------------------------------------------------------------------------------------------------------------
    # client...

    def start(self):
        return None


    @abstractmethod
    def next_params(self, params):
        pass


    @property
    @abstractmethod
    def next_url(self):
        pass
