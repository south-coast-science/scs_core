"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

www.alphasense-technology.co.uk...
{"sensor_type":"PIDH2","serial_number":"143370503","we_electronic_zero_mv":"n/a","we_sensor_zero_mv":"61.88",
"we_total_zero_mv":"n/a","ae_electronic_zero_mv":"n/a","ae_sensor_zero_mv":"n/a","ae_total_zero_mv":"n/a",
"we_sensitivity_na_ppb":"n/a","we_cross_sensitivity_no2_na_ppb":"n/a","pcb_gain":"n/a",
"we_sensitivity_mv_ppb":"51.68","we_cross_sensitivity_no2_mv_ppb":"n/a","calibration_date":"2022-05-10"}
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
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        if 'pid_zero_mv' in jdict:
            pid_elc_mv = jdict.get('pid_zero_mv')
        else:
            pid_elc_mv = jdict.get('we_sensor_zero_mv')

        if 'pid_sensitivity_mv_ppm' in jdict:
            pid_sens_mv_ppm = jdict.get('pid_sensitivity_mv_ppm')
        else:
            pid_sens_mv_ppm = jdict.get('we_sensitivity_mv_ppb')        # uses mV / ppb field to record mV / ppm

        return cls(serial_number, sensor_type, pid_elc_mv, pid_sens_mv_ppm)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, pid_elc_mv, pid_sens_mv_ppm):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__pid_elc_mv = Datum.float(pid_elc_mv, 3)                  # PID electronic zero           mV
        self.__pid_sens_mv_ppm = Datum.float(pid_sens_mv_ppm, 6)        # PID sensitivity               mV / ppm

        self.validate()


    def __eq__(self, other):
        try:
            return self.serial_number == other.serial_number and self.sensor_type == other.sensor_type and \
                   self.pid_elc_mv == other.pid_elc_mv and self.pid_sens_mv_ppm == other.pid_sens_mv_ppm

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self):
        if self.pid_sens_mv_ppm == 0.0:
            raise ValueError('%s - pid_sensitivity_mv_ppm: zero sensitivity' % self.sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    def set_defaults(self):
        pass                                # PID may have null values


    def set_sens_mv_from_sens_na(self):
        pass                                # sensitivity nA data is not available


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['pid_zero_mv'] = self.pid_elc_mv
        jdict['pid_sensitivity_mv_ppm'] = self.pid_sens_mv_ppm

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pid_elc_mv(self):
        return self.__pid_elc_mv


    @property
    def pid_sens_v_ppb(self):
        return self.__pid_sens_mv_ppm / 1000000.0


    @property
    def pid_sens_mv_ppm(self):
        return self.__pid_sens_mv_ppm


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalib:{serial_number:%s, sensor_type:%s, pid_elc_mv:%s, pid_sens_mv_ppm:%s}" % \
                    (self.serial_number, self.sensor_type, self.pid_elc_mv, self.pid_sens_mv_ppm)
