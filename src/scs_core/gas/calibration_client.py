"""
Created on 7 May 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from abc import ABC

from scs_core.client.http_client import HTTPClient
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CalibrationClient(ABC):
    """
    classdocs
    """

    __HOST =       "calibration.southcoastscience.com"
    __HEADER =     {"Accept": "application/json"}

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path):
        self.__path = path
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def download(self, serial_number):
        http_client = HTTPClient()
        http_client.connect(self.__HOST)

        try:
            path = self.path + serial_number
            response = http_client.get(path, None, self.__HEADER)

            self.__logger.debug("response: %s" % response)

            return json.loads(response)

        finally:
            http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{host:%s, path:%s}" %  (self.__HOST, self.path)


# --------------------------------------------------------------------------------------------------------------------

class AFECalibrationClient(CalibrationClient):
    """
    classdocs
    """

    __PATH =       "/api/v1/boards/"

    @classmethod
    def construct(cls):
        return cls(cls.__PATH)


# --------------------------------------------------------------------------------------------------------------------

class SensorCalibrationClient(CalibrationClient):
    """
    classdocs
    """

    __PATH =       "/api/v1/sensors/"

    @classmethod
    def construct(cls):
        return cls(cls.__PATH)
