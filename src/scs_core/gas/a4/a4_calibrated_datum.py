"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a4_calibrated_datum.py is aligned to a4_calibrated_datum_vB.py

The A4CalibratedDatum is designed to provide a model training data set that encapsulates the calibration of the
electrochemical sensor. v_x_cal is only relevant to sensors with NO2 cross-sensitivity.

example document:
{"weV": 0.30338, "aeV": 0.27969, "weC": 2e-05, "cnc": 0.1, "weVz": 0.00738, "aeVz": 0.00469, "vCal": 9.087838}
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
        self.__calib = calib                                                # A4Calib

        self.__we_elc_v = calib.we_elc_mv / 1000.0                          # we_electronic_zero_mv
        self.__ae_elc_v = calib.ae_elc_mv / 1000.0                          # ae_electronic_zero_mv

        self.__we_sens_v = calib.we_sens_mv / 1000.0                        # we_sensitivity_mv_ppb

        self.__we_no2_x_sens_v = None if calib.we_no2_x_sens_mv is None else calib.we_no2_x_sens_mv / 1000.0


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum, no2_cnc=None):
        # zero offset...
        we_v_zero_cal = datum.we_v - self.__we_elc_v
        ae_v_zero_cal = datum.ae_v - self.__ae_elc_v

        # remove noise...
        v_zero_cal = we_v_zero_cal - ae_v_zero_cal

        # gain...
        v_cal = v_zero_cal / self.__we_sens_v

        # cross sensitivity...
        v_x_cal = None if no2_cnc is None else no2_cnc * self.__we_no2_x_sens_v

        return A4CalibratedDatum(datum.we_v, datum.ae_v, datum.we_c, datum.cnc,
                                 we_v_zero_cal, ae_v_zero_cal, v_cal, v_x_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calibrator:{calib:%s}" % self.__calib


# --------------------------------------------------------------------------------------------------------------------

class A4CalibratedDatum(A4Datum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, we_v_zero_cal, ae_v_zero_cal, v_cal, v_x_cal):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__we_v_zero_cal = Datum.float(we_v_zero_cal, 6)        # zero-offset-corrected WE voltage
        self.__ae_v_zero_cal = Datum.float(ae_v_zero_cal, 6)        # zero-offset-corrected AE voltage

        self.__v_cal = Datum.float(v_cal, 6)                        # calibrated voltage
        self.__v_x_cal = Datum.float(v_x_cal, 9)                    # calibrated cross-sensitivity voltage


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                                # may be None
        jdict['cnc'] = self.cnc                                 # may be None

        jdict['weVz'] = self.we_v_zero_cal
        jdict['aeVz'] = self.ae_v_zero_cal

        jdict['vCal'] = self.v_cal

        if self.v_x_cal is not None:
            jdict['vXCal'] = self.v_x_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_v_zero_cal(self):
        return self.__we_v_zero_cal


    @property
    def ae_v_zero_cal(self):
        return self.__ae_v_zero_cal


    @property
    def v_cal(self):
        return self.__v_cal


    @property
    def v_x_cal(self):
        return self.__v_x_cal


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum:{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, " \
               "we_v_zero_cal:%s, ae_v_zero_cal:%s, v_cal:%s, v_x_cal:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc,
                self.we_v_zero_cal, self.ae_v_zero_cal, self.v_cal, self.v_x_cal)
