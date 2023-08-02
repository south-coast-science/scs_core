"""
Created on 19 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from abc import ABC, abstractmethod
from http import HTTPStatus

from scs_core.client.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class APIClient(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        """
        Constructor
        """
        self.__reporter = reporter
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def _auth_headers(self, auth):
        header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Authorization": auth}
        self.__logger.debug('header: %s' % header)

        return header


    def _token_headers(self, token):
        header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Token": token}
        self.__logger.debug('header: %s' % header)

        return header


    def _check_response(self, response):
        self.__logger.debug('response.json: %s' % response.json())

        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def _get_blocks(self, url, token, params, block_class):
        while True:
            response = requests.get(url, headers=self._token_headers(token), params=params)
            self._check_response(response)

            # messages...
            block = block_class.construct_from_jdict(response.json())
            self.__logger.debug(block)

            for item in block.items:
                yield item

            # report...
            if self.__reporter:
                self.__reporter.print(len(block), block_start=block.start())

            # next request...
            if block.next_url is None:
                break

            params = block.next_params(params)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def _reporter(self):
        return self.__reporter


    @property
    def _logger(self):
        return self.__logger


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{reporter:%s}" % self.__reporter


# --------------------------------------------------------------------------------------------------------------------

class APIResponse(ABC):
    """
    classdocs
    """

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def next_params(self, params):
        pass


    @property
    @abstractmethod
    def next_url(self):
        pass
