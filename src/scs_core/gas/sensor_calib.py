"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC

from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class SensorCalib(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def reports_no2_cross_sensitivity(cls):     # the default - override as necessary
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type):
        """
        Constructor
        """
        self.__serial_number = serial_number            # int
        self.__sensor_type = sensor_type                # string


    # ----------------------------------------------------------------------------------------------------------------

    def sensor(self, baseline):
        sensor = Sensor.find(self.__serial_number)

        sensor.calib = self
        sensor.baseline = baseline

        return sensor


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def sensor_type(self):
        return self.__sensor_type

