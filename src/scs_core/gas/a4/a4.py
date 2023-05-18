"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense A4 electrochemical sensor
"""

from scs_core.gas.sensor import Sensor

from scs_core.gas.a4.a4_calibrated_datum import A4Calibrator
from scs_core.gas.a4.a4_datum import A4Datum
from scs_core.gas.a4.a4_temp_comp import A4TempComp


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
        cls.SENSORS[cls.CODE_NO2] =     A4(cls.CODE_NO2,    'NO2A43F',  'NO2',  3)      # was NOGA4
        cls.SENSORS[cls.CODE_OX] =      A4(cls.CODE_OX,     'OXA431',   'Ox',   3)      # was OXGA4, ref in A4Calib
        cls.SENSORS[cls.CODE_SO2] =     A4(cls.CODE_SO2,    'SO2A4',    'SO2',  3)

        cls.SENSORS[cls.CODE_VOCe] =    A4(cls.CODE_VOCe,   'VOCA4',    'VOCe', 3)

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
                raise ValueError("NO2 sample required, but none given.")

            return self.datum(temp, we_v, ae_v, no2_cnc=no2_sample.cnc)

        return self.datum(temp, we_v, ae_v)


    def datum(self, temp, we_v, ae_v, no2_cnc=None):
        datum = A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v, no2_cnc=no2_cnc)

        if self.calibrator is None:
            return datum

        return self.calibrator.calibrate(datum)     # no2_cnc is not supplied here - wait for the exegesis NO2 value


    def null_datum(self):
        return A4Datum(None, None)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tc(self):
        return self.__tc


    @property
    def calib(self):
        return self._calib


    @calib.setter
    def calib(self, calib):
        self._calib = calib
        self._calibrator = A4Calibrator(calib)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4:{sensor_code:%s, sensor_type:%s, gas_name:%s, calib:%s, baseline:%s, tc:%s, calibrator:%s}" %  \
               (self.sensor_code, self.sensor_type, self.gas_name, self.calib, self.baseline, self.tc, self.calibrator)
