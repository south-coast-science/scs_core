"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.a4_datum import A4Datum
from scs_core.gas.sensor import Sensor
from scs_core.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

class A4(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.SENSORS[cls.CODE_CO] =      A4(cls.CODE_CO,     'CO',   3)
        cls.SENSORS[cls.CODE_H2S] =     A4(cls.CODE_H2S,    'H2S',  3)
        cls.SENSORS[cls.CODE_NO] =      A4(cls.CODE_NO,     'NO',   3)
        cls.SENSORS[cls.CODE_NO2] =     A4(cls.CODE_NO2,    'NO2',  3)
        cls.SENSORS[cls.CODE_OX] =      A4(cls.CODE_OX,     'Ox',   3)
        cls.SENSORS[cls.CODE_SO2] =     A4(cls.CODE_SO2,    'SO2',  3)

        cls.SENSORS[cls.CODE_TEST_1] =  A4(cls.CODE_TEST_1, 'SN1',  3)
        cls.SENSORS[cls.CODE_TEST_2] =  A4(cls.CODE_TEST_2, 'SN2',  3)
        cls.SENSORS[cls.CODE_TEST_3] =  A4(cls.CODE_TEST_3, 'SN3',  3)
        cls.SENSORS[cls.CODE_TEST_4] =  A4(cls.CODE_TEST_4, 'SN4',  3)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_code, gas_name, adc_gain_index):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_code, gas_name, adc_gain_index)

        self.__tc = TempComp.find(sensor_code)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, sensor_index, no2_sample=None):
        we_v, ae_v = afe.sample_raw_wrk_aux(sensor_index, self.adc_gain_index)

        if self.has_no2_cross_sensitivity():
            if no2_sample is None:
                raise ValueError("A4.sample: no2_sample required, but none given.")

            return A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v, no2_sample.cnc)

        return A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4:{sensor_code:%s, gas_name:%s, adc_gain_index:0x%04x, calib:%s, baseline:%s, tc:%s}" %  \
               (self.sensor_code, self.gas_name, self.adc_gain_index, self.calib, self.baseline, self.__tc)
