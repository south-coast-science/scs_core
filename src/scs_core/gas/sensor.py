"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.alphasense-technology.co.uk/sensor_types
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Sensor(ABC):
    """
    classdocs
    """

    CODE_CO =           '132'           # CO A4
    CODE_H2S =          '133'           # H2SA4
    CODE_NO =           '130'           # NO A4
    CODE_NO2 =          '212'           # NOGA4
    CODE_OX =           '214'           # OXGA4
    CODE_SO2 =          '134'           # SO2A4

    CODE_VOC_PPM =      '142'           # PID-A12
    CODE_VOC_PPB_T1 =   '143'           # PID-AH
    CODE_VOC_PPB_T2 =   '354'           # PID-AH (since June 2019)
    CODE_VOC_PPB_T3 =   '401'           # PID-AH (since April 2020)

    CODE_TEST_1 =       '01'            # test load
    CODE_TEST_2 =       '02'            # test load
    CODE_TEST_3 =       '03'            # test load
    CODE_TEST_4 =       '04'            # test load

    SENSORS =       {}


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find(cls, serial_number):
        if serial_number is None:
            return None

        for code, sensor in cls.SENSORS.items():
            if str(serial_number).startswith(code):
                return sensor

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_code, sensor_type, gas_name, adc_gain_index, calib=None, baseline=None):
        """
        Constructor
        """
        self.__sensor_code = sensor_code
        self.__sensor_type = sensor_type

        self.__gas_name = gas_name
        self.__adc_gain_index = adc_gain_index

        self._calib = calib
        self.__baseline = baseline


    # ----------------------------------------------------------------------------------------------------------------

    def has_no2_cross_sensitivity(self):
        if self.calib is None:
            return False

        return self.calib.reports_no2_cross_sensitivity() and self.gas_name != 'NO2'


    @abstractmethod
    def sample(self, afe, temp, index, no2_sample=None):
        pass


    @abstractmethod
    def null_datum(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensor_code(self):
        return self.__sensor_code


    @property
    def sensor_type(self):
        return self.__sensor_type


    @property
    def gas_name(self):
        return self.__gas_name


    @property
    def adc_gain_index(self):
        return self.__adc_gain_index


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calib(self):
        return self._calib


    @calib.setter
    def calib(self, calib):             # TODO: override this in PID, to use defaults
        self._calib = calib


    @property
    def baseline(self):
        return self.__baseline


    @baseline.setter
    def baseline(self, baseline):
        self.__baseline = baseline
