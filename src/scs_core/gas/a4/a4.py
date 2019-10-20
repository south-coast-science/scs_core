"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense A4 electrochemical sensor
"""

from scs_core.gas.a4.a4_datum import A4Datum
from scs_core.gas.a4.a4_temp_comp import A4TempComp

from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class A4(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.SENSORS[cls.CODE_CO] =      A4(cls.CODE_CO,     'CO A4',    'CO',   3)
        cls.SENSORS[cls.CODE_H2S] =     A4(cls.CODE_H2S,    'H2SA4',    'H2S',  3)
        cls.SENSORS[cls.CODE_NO] =      A4(cls.CODE_NO,     'NO A4',    'NO',   3)
        cls.SENSORS[cls.CODE_NO2] =     A4(cls.CODE_NO2,    'NOGA4',    'NO2',  3)
        cls.SENSORS[cls.CODE_OX] =      A4(cls.CODE_OX,     'OXGA4',    'Ox',   3)
        cls.SENSORS[cls.CODE_SO2] =     A4(cls.CODE_SO2,    'SO2A4',    'SO2',  3)

        cls.SENSORS[cls.CODE_TEST_1] =  A4(cls.CODE_TEST_1, 'TEST',     'SN1',  3)
        cls.SENSORS[cls.CODE_TEST_2] =  A4(cls.CODE_TEST_2, 'TEST',     'SN2',  3)
        cls.SENSORS[cls.CODE_TEST_3] =  A4(cls.CODE_TEST_3, 'TEST',     'SN3',  3)
        cls.SENSORS[cls.CODE_TEST_4] =  A4(cls.CODE_TEST_4, 'TEST',     'SN4',  3)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_code, sensor_type, gas_name, adc_gain_index):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_code, sensor_type, gas_name, adc_gain_index)

        self.__tc = A4TempComp.find(sensor_code)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, sensor_index, no2_sample=None):
        we_v, ae_v = afe.sample_raw_wrk_aux(sensor_index, self.adc_gain_index)

        if self.has_no2_cross_sensitivity():
            if no2_sample is None:
                raise ValueError("A4.sample: no2_sample required, but none given.")

            return A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v, no2_sample.cnc)

        return A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v)


    def null_datum(self):
        return A4Datum(None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4:{sensor_code:%s, sensor_type:%s, gas_name:%s, calib:%s, baseline:%s}" %  \
               (self.sensor_code, self.sensor_type, self.gas_name, self.calib, self.baseline)
