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

    ALPHASENSE_HOST =       "www.alphasense-technology.co.uk"
    ALPHASENSE_PATH =       "/api/v1/sensors/"
    ALPHASENSE_HEADER =     {"Accept": "application/json"}


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        # late import...
        from scs_core.gas.a4.a4_calib import A4Calib
        from scs_core.gas.pid.pid_calib import PIDCalib

        sensor_type = jdict.get('sensor_type', 'NOGA4')

        if sensor_type[-2:] == 'A4' or sensor_type[:2] == 'SN':
            return A4Calib.construct_from_jdict(jdict)

        elif sensor_type[:3] == 'PID':
            return PIDCalib.construct_from_jdict(jdict)

        raise ValueError(sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def reports_no2_cross_sensitivity(cls):             # the default - override as necessary
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


    @serial_number.setter
    def serial_number(self, serial_number):
        self.__serial_number = serial_number


    @property
    def sensor_type(self):
        return self.__sensor_type


    @sensor_type.setter
    def sensor_type(self, sensor_type):
        self.__sensor_type = sensor_type

