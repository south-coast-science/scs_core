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
        cls.SENSORS[cls.CODE_VOC_PPM] = PID(cls.CODE_VOC_PPM,  'VOC',  4)
        cls.SENSORS[cls.CODE_VOC_PPB] = PID(cls.CODE_VOC_PPB,  'VOC',  4)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain_index):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_type, gas_name, adc_gain_index)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, sensor_index, no2_sample=None):
        wrk = afe.sample_raw_wrk(sensor_index, self.adc_gain_index)

        # TODO handle PID calib and baseline for cnc

        return PIDDatum(wrk)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PID:{sensor_code:%s, gas_name:%s, adc_gain_index:0x%04x, calib:%s, baseline:%s}" % \
                        (self.sensor_code, self.gas_name, self.adc_gain_index, self.calib, self.baseline)
