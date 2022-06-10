"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The A4CalibratedDatum is a normalised electrochem output voltage. Its vCal field represents the calibrated weV
minus the calibrated aeV.

(Obsolete: The vXCal field should only be computed when the NO2 concentration is known precisely, so this should be
done in the preprocessing phase for the O3 model.)

example document:
{"weV": 0.39519, "aeV": 0.39963, "weC": 0.00627, "cnc": 61.9, "vCal": -9.801, "xCal": -12.601}
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

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib: A4Calib):
        """
        Constructor
        """
        self.__we_elc_v = round(calib.we_elc_mv / 1000.0, 3)                        # we_electronic_zero_mv
        self.__ae_elc_v = round(calib.ae_elc_mv / 1000.0, 3)                        # ae_electronic_zero_mv

        self.__we_sens_v = round(calib.we_sens_mv / 1000.0, 6)                      # we_sensitivity_mv_ppb

        if calib.is_ox_sensor():
            self.__we_no2_x_sens_v = round(calib.we_no2_x_sens_mv / 1000.0, 6)      # we_cross_sensitivity_no2_mv_ppb
        else:
            self.__we_no2_x_sens_v = None


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum):
        v_cal = self.__calibrate(datum, self.we_sens_v)
        x_cal = self.__calibrate(datum, self.we_no2_x_sens_v)

        return A4CalibratedDatum(datum.we_v, datum.ae_v, datum.we_c, datum.cnc, v_cal, x_cal=x_cal)


    def __calibrate(self, datum, we_sens_v):
        if we_sens_v is None:
            return None

        # zero offset...
        we_v_zero_cal = datum.we_v - self.we_elc_v
        ae_v_zero_cal = datum.ae_v - self.ae_elc_v

        # remove noise...
        v_zero_cal = we_v_zero_cal - ae_v_zero_cal

        # gain...
        return v_zero_cal / we_sens_v


    def set_we_v_zero_x_cal(self, datum, no2_cnc):
        # we_v_x = no2_cnc * self.we_no2_x_sens_v
        # datum.we_v_zero_x_cal = we_v_x - self.we_elc_v
        pass


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
        x_cal = jdict.get('xCal')

        return cls(we_v, ae_v, we_c, cnc, v_cal, x_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, v_cal, x_cal=None):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__v_cal = Datum.float(v_cal, 3)                        # calibrated ppb
        self.__x_cal = Datum.float(x_cal, 3)                        # calibrated ppb according to cross-sensitivity


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v
        jdict['weC'] = self.we_c                                # may be None
        jdict['cnc'] = self.cnc                                 # may be None

        if self.v_cal is not None:
            jdict['vCal'] = self.v_cal

        if self.x_cal is not None:
            jdict['xCal'] = self.x_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def v_cal(self):
        return self.__v_cal


    @property
    def x_cal(self):
        return self.__x_cal


    # @x_cal.setter
    # def x_cal(self, x_cal):
    #     self.__x_cal = round(x_cal, 9)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum:{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, v_cal:%s, x_cal:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc, self.v_cal, self.x_cal)
