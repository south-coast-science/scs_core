"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod

from scs_core.data.json import JSONable
from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class SensorCalib(ABC, JSONable):
    """
    classdocs
    """

    ALPHASENSE_HOST =       "www.alphasense-technology.co.uk"
    ALPHASENSE_PATH =       "/api/v1/sensors/"
    ALPHASENSE_HEADER =     {"Accept": "application/json"}


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        from scs_core.gas.a4.a4_calib import A4Calib            # late import
        from scs_core.gas.pid.pid_calib import PIDCalib         # late import

        sensor_type = jdict.get('sensor_type', 'NOGA4')

        if 'A4' in sensor_type or sensor_type.startswith('SN'):
            return A4Calib.construct_from_jdict(jdict)

        elif sensor_type.startswith('PID'):
            return PIDCalib.construct_from_jdict(jdict)

        raise ValueError(sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_no2_cross_sensitivity(cls):                     # the default - override as necessary
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type):
        """
        Constructor
        """
        self.__serial_number = serial_number                    # int
        self.__sensor_type = sensor_type                        # string


    def __eq__(self, other):
        try:
            return self.serial_number == other.serial_number and self.sensor_type == other.sensor_type

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def validate(self):
        pass


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


    @serial_number.setter
    def serial_number(self, serial_number):
        self.__serial_number = serial_number


    @property
    def sensor_type(self):
        return self.__sensor_type


    @sensor_type.setter
    def sensor_type(self, sensor_type):
        self.__sensor_type = sensor_type

