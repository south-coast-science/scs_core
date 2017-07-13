"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class PIDCalib(SensorCalib):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        pid_elc = jdict.get('pid_zero_mv')
        pid_sens = jdict.get('pid_sensitivity_mv_ppm')

        return PIDCalib(serial_number, sensor_type, pid_elc, pid_sens)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, pid_elc, pid_sens):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__pid_elc = Datum.int(pid_elc)                 # PID electronic zero                   mV
        self.__pid_sens = Datum.float(pid_sens, 3)          # PID sensitivity                       mV / ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['pid_zero_mv'] = self.pid_elc
        jdict['pid_sensitivity_mv_ppm'] = self.pid_sens

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pid_elc(self):
        return self.__pid_elc


    @property
    def pid_sens(self):
        return self.__pid_sens


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalib:{serial_number:%s, sensor_type:%s, pid_elc:%s, pid_sens:%s}" % \
                    (self.serial_number, self.sensor_type, self.pid_elc, self.pid_sens)
