"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.pid_datum import PIDDatum
from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class PID(Sensor):
    """
    classdocs
    """



    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.SENSORS[cls.CODE_VOC_PPM] = PID(cls.CODE_VOC_PPM,  'VOC',  4, 50, 400)      # ppb sensitivity
        cls.SENSORS[cls.CODE_VOC_PPB] = PID(cls.CODE_VOC_PPB,  'VOC',  4, 50, 30)       # ppb sensitivity


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain_index, default_elc, default_sens):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_type, gas_name, adc_gain_index)

        self.__default_elc = default_elc
        self.__default_sens = default_sens


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, sensor_index, no2_sample=None):
        wrk = afe.sample_raw_wrk(sensor_index, self.adc_gain_index)

        # TODO handle PID calib and baseline for cnc

        print("sample: %s" % self)

        return PIDDatum(wrk)


    def null_datum(self):
        return PIDDatum(None)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def default_elc(self):
        return self.__default_elc

    @property
    def default_sens(self):
        return self.__default_elc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PID:{sensor_code:%s, gas_name:%s, adc_gain_index:0x%04x, default_elc:%s, default_sens:%s, " \
               "calib:%s, baseline:%s}" %  \
               (self.sensor_code, self.gas_name, self.adc_gain_index, self.default_elc, self.default_sens,
                self.calib, self.baseline)
