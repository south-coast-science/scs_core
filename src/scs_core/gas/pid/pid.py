"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense A4 photo ionisation detector

PID-AH sn: 143950149 - pid_elc_mv: 47.6, pid_sens_mv_ppm: 0.0375

PID-AH "default" - pid_elc_mv: 54, pid_sens_mv_ppm: 0.040
"""

from scs_core.gas.pid.pid_calib import PIDCalib
from scs_core.gas.pid.pid_calibrated_datum import PIDCalibrator
from scs_core.gas.pid.pid_datum import PIDDatum
from scs_core.gas.pid.pid_temp_comp import PIDTempComp

from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class PID(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    #

    @classmethod
    def init(cls):
        # ppb sensitivity...
        cls.SENSORS[cls.CODE_VOC_PPB_T1] = PID(cls.CODE_VOC_PPB_T1,  'PIDH2', 'VOC',  4, 50.0, 40.0)    # was PIDNH
        cls.SENSORS[cls.CODE_VOC_PPB_T2] = PID(cls.CODE_VOC_PPB_T2,  'PIDH2', 'VOC',  4, 50.0, 40.0)    # was PIDNH
        cls.SENSORS[cls.CODE_VOC_PPB_T3] = PID(cls.CODE_VOC_PPB_T2,  'PIDH2', 'VOC',  4, 50.0, 40.0)    # was PIDNH
        cls.SENSORS[cls.CODE_VOC_PPB_T4] = PID(cls.CODE_VOC_PPB_T2,  'PIDH2', 'VOC',  4, 50.0, 40.0)    # was PIDNH
        cls.SENSORS[cls.CODE_VOC_PPB_T5] = PID(cls.CODE_VOC_PPB_T2,  'PIDH2', 'VOC',  4, 50.0, 40.0)    # was PIDNH

        # ppm sensitivity
        cls.SENSORS[cls.CODE_VOC_PPM] = PID(cls.CODE_VOC_PPM,  'VOC',  'PID12', 4, 50.0, 0.040)     # was PIDN1


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_code, sensor_type, gas_name, adc_gain_index, default_elc_mv, default_sens_mv_ppm):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_code, sensor_type, gas_name, adc_gain_index)

        self.__default_elc_mv = default_elc_mv
        self.__default_sens_mv_ppm = default_sens_mv_ppm

        self.__tc = PIDTempComp.find(sensor_code)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, sensor_index, no2_sample=None):
        we_v = afe.sample_raw_wrk(sensor_index, self.adc_gain_index)

        datum = PIDDatum.construct(self.calib, self.baseline, self.__tc, temp, we_v)

        if self.calibrator is None:
            return datum

        return self.calibrator.calibrate(datum)


    def null_datum(self):
        return PIDDatum(None)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def default_elc_mv(self):
        return self.__default_elc_mv


    @property
    def default_sens_mv_ppm(self):
        return self.__default_sens_mv_ppm


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calib(self):
        return self._calib


    @calib.setter
    def calib(self, calib):
        # replace missing values with defaults...
        pid_elc_mv = self.default_elc_mv if calib.pid_elc_mv is None else calib.pid_elc_mv
        pid_sens_mv_ppm = self.default_sens_mv_ppm if calib.pid_sens_mv_ppm is None else calib.pid_sens_mv_ppm

        # set calibration...
        self._calib = PIDCalib(calib.serial_number, calib.sensor_type, pid_elc_mv, pid_sens_mv_ppm)
        self._calibrator = PIDCalibrator(self.calib)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PID:{sensor_code:%s, sensor_type:%s, gas_name:%s, adc_gain_index:0x%04x, default_elc_mv:%s, " \
               "default_sens_mv_ppm:%s, calib:%s, baseline:%s}" %  \
               (self.sensor_code, self.sensor_type, self.gas_name, self.adc_gain_index, self.default_elc_mv,
                self.default_sens_mv_ppm, self.calib, self.baseline)
