"""
Created on 23 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/http.html
https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
"""

from abc import ABC
from http import HTTPStatus

from scs_core.client.http_exception import HTTPException
from scs_core.data.json import JSONable, JSONify


# --------------------------------------------------------------------------------------------------------------------

class HTTPResponse(JSONable, ABC):
    """
    classdocs
    """

    __CORS_HEADERS = {                                  # Cross-Origin Resource Sharing
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True,
    }


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_res(cls, response):         # response: requests.Response
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())

        jdict = response.json()

        if not jdict:
            return None

        return cls.construct_from_response_jdict(status, jdict)


    @classmethod
    def construct_from_response_jdict(cls, status, jdict):
        return cls(status, body=jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, body=None):
        """
        Constructor
        """
        self.__status = status                          # HTTPStatus member
        self.__body = body                              # string


    def __len__(self):
        try:
            return len(self.body)
        except (AttributeError, TypeError):
            return 1


    # ----------------------------------------------------------------------------------------------------------------

    def is_ok(self):
        return self.status == HTTPStatus.OK


    # ----------------------------------------------------------------------------------------------------------------

    def as_http(self, cors=False):
        jdict = {
            'statusCode': int(self.status),
            'body': JSONify.dumps(self)
        }

        if cors:
            jdict['headers'] = self.__CORS_HEADERS

        return jdict


    def as_json(self):
        return self.body


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        return self.__status


    @property
    def body(self):
        return self.__body


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HTTPResponse:{status:%s, body:%s}" % (self.status, self.body)
