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
    def construct_from_jdict(cls, jdict, default=True):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        pid_elc_mv = jdict.get('pid_zero_mv')
        pid_sens_mv = jdict.get('pid_sensitivity_mv_ppm')

        return cls(serial_number, sensor_type, pid_elc_mv, pid_sens_mv)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, pid_elc_mv, pid_sens_mv):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__pid_elc_mv = Datum.int(pid_elc_mv)                 # PID electronic zero                   mV
        self.__pid_sens_mv = Datum.float(pid_sens_mv, 6)          # PID sensitivity                       mV / ppm


    def __eq__(self, other):
        try:
            return self.serial_number == other.serial_number and self.sensor_type == other.sensor_type and \
                   self.pid_elc_mv == other.pid_elc_mv and self.pid_sens_mv == other.pid_sens_mv

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['pid_zero_mv'] = self.pid_elc_mv
        jdict['pid_sensitivity_mv_ppm'] = self.pid_sens_mv

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pid_elc_mv(self):
        return self.__pid_elc_mv


    @property
    def pid_sens_mv(self):
        return self.__pid_sens_mv


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalib:{serial_number:%s, sensor_type:%s, pid_elc_mv:%s, pid_sens_mv:%s}" % \
                    (self.serial_number, self.sensor_type, self.pid_elc_mv, self.pid_sens_mv)
