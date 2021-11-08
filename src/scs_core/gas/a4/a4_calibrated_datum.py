"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The A4CalibratedDatum is a normalised electrochem output voltage. Its vCal field represents the calibrated weV
minus the calibrated aeV.

The vXCal field should only be computed when the NO2 concentration is known precisely, so this should be done
in the preprocessing phase for the O3 model.

example document:
{"weV": 0.41138, "aeV": 0.40257, "weC": 0.02671, "cnc": 116.5, "vCal": 17.292, "vXCal": 0.00212}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum

from scs_core.gas.a4.a4_calib import A4Calib
from scs_core.gas.a4.a4_datum import A4Datum


# --------------------------------------------------------------------------------------------------------------------

class A4Calibrator(object):
    """
    classdocs
    """

    __CALIBRATED_GASES = ('CO', 'H2S', 'NO', 'NO2', 'Ox', 'SO2', 'VOCe')

    @classmethod
    def calibrated_gases(cls):
        return cls.__CALIBRATED_GASES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib: A4Calib):
        """
        Constructor
        """
        self.__we_elc_v = round(calib.we_elc_mv / 1000.0, 3)                        # we_electronic_zero_mv
        self.__ae_elc_v = round(calib.ae_elc_mv / 1000.0, 3)                        # ae_electronic_zero_mv

        self.__we_sens_v = round(calib.we_sens_mv / 1000.0, 6)                      # we_sensitivity_mv_ppb

        if calib.we_no2_x_sens_mv is None:
            self.__we_no2_x_sens_v = None
        else:
            self.__we_no2_x_sens_v = round(calib.we_no2_x_sens_mv / 1000.0, 6)      # we_cross_sensitivity_no2_mv_ppb


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum):
        # zero offset...
        we_v_zero_cal = datum.we_v - self.we_elc_v
        ae_v_zero_cal = datum.ae_v - self.ae_elc_v

        # remove noise...
        v_zero_cal = we_v_zero_cal - ae_v_zero_cal

        # gain...
        v_cal = v_zero_cal / self.we_sens_v

        return A4CalibratedDatum(datum.we_v, datum.ae_v, datum.we_c, datum.cnc, v_cal)


    def set_we_v_zero_x_cal(self, datum, no2_cnc):
        we_v_x = no2_cnc * self.we_no2_x_sens_v
        datum.we_v_zero_x_cal = we_v_x - self.we_elc_v


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_elc_v(self):
        return self.__we_elc_v


    @property
    def ae_elc_v(self):
        return self.__ae_elc_v


    @property
    def we_sens_v(self):
        return self.__we_sens_v


    @property
    def we_no2_x_sens_v(self):
        return self.__we_no2_x_sens_v


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calibrator:{we_elc_v:%s, ae_elc_v:%s, we_sens_v:%s, we_no2_x_sens_v:%s}" % \
               (self.we_elc_v, self.ae_elc_v, self.we_sens_v, self.we_no2_x_sens_v)


# --------------------------------------------------------------------------------------------------------------------

class A4CalibratedDatum(A4Datum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        we_v = jdict.get('weV')
        ae_v = jdict.get('aeV')

        we_c = jdict.get('weC')
        cnc = jdict.get('cnc')

        v_cal = jdict.get('vCal')
        we_v_zero_x_cal = jdict.get('xCal')

        return cls(we_v, ae_v, we_c, cnc, v_cal, we_v_zero_x_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, v_cal, we_v_zero_x_cal=None):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__v_cal = Datum.float(v_cal, 3)                            # calibrated voltage (ppb)
        self.__we_v_zero_x_cal = Datum.float(we_v_zero_x_cal, 6)        # response to NO2 cross-sensitivity (Volts)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                                # may be None
        jdict['cnc'] = self.cnc                                 # may be None

        if self.v_cal is not None:
            jdict['vCal'] = self.v_cal

        if self.we_v_zero_x_cal is not None:
            jdict['xCal'] = self.we_v_zero_x_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def v_cal(self):
        return self.__v_cal


    @property
    def we_v_zero_x_cal(self):
        return self.__we_v_zero_x_cal


    @we_v_zero_x_cal.setter
    def we_v_zero_x_cal(self, we_v_zero_x_cal):
        self.__we_v_zero_x_cal = round(we_v_zero_x_cal, 9)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum:{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, v_cal:%s, we_v_zero_x_cal:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc, self.v_cal, self.we_v_zero_x_cal)
