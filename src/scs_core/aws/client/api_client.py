"""
Created on 19 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC
from http import HTTPStatus

from scs_core.client.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class APIClient(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        """
        Constructor
        """
        self.__http_client = http_client                        # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def _auth_headers(self, auth):
        header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Authorization": auth}
        self.__logger.debug('headers: %s' % header)

        return header


    def _token_headers(self, token):
        header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Token": token}
        self.__logger.debug('headers: %s' % header)

        return header


    def _check_response(self, response):
        self.__logger.debug('response.json: %s' % response.json())

        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def _http_client(self):
        return self.__http_client


    @property
    def _logger(self):
        return self.__logger


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{http_client:%s}" % self._http_client
