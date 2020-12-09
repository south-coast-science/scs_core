"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The A4CalibratedDatum provides a training data set that encapsulates the calibration of the electrochemical sensor.
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.gas.a4.a4_datum import A4Datum


# --------------------------------------------------------------------------------------------------------------------

class A4Calibrator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib):
        """
        Constructor
        """
        self.__calib = calib                                                # A4Calib

        self.__we_elc_v = calib.we_elc_mv / 1000.0
        self.__ae_elc_v = calib.ae_elc_mv / 1000.0

        self.__we_sens_v = calib.we_sens_mv / 1000.0
        self.__we_no2_x_sens_v = calib.we_no2_x_sens_mv / 1000.0


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum, no2_cnc=None):
        # zero offset...
        we_v_zero_cal = datum.we_v - self.__we_elc_v
        ae_v_zero_cal = datum.ae_v - self.__ae_elc_v

        # print("         ae_v: %s" % datum.ae_v)
        # print("ae_v_zero_cal: %s" % ae_v_zero_cal)
        # print("         we_v: %s" % datum.we_v)
        # print("we_v_zero_cal: %s" % we_v_zero_cal)
        # print("-")

        # noise rejection...
        v = we_v_zero_cal - ae_v_zero_cal

        # print("           v1: %s" % v)
        # print("-")

        # gain...
        cal_v = v / self.__we_sens_v

        # cross sensitivity...
        cal_x_v = None if no2_cnc is None else no2_cnc * self.__we_no2_x_sens_v

        return A4CalibratedDatum(datum.we_v, datum.ae_v, datum.we_c, datum.cnc, cal_v, cal_x_v)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calibrator:{calib:%s}" % self.__calib


# --------------------------------------------------------------------------------------------------------------------

class A4CalibratedDatum(A4Datum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, cal_v, cal_x_v):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__cal_v = Datum.float(cal_v, 5)                # calibrated voltage
        self.__cal_x_v = Datum.float(cal_x_v, 9)            # calibrated cross-sensitivity voltage


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                            # may be None
        jdict['cnc'] = self.cnc                             # may be None

        jdict['calV'] = self.cal_v

        if self.cal_x_v is not None:
            jdict['calXV'] = self.cal_x_v

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cal_v(self):
        return self.__cal_v


    @property
    def cal_x_v(self):
        return self.__cal_x_v


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum:{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, cal_v:%s, cal_x_v:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc, self.cal_v, self.cal_x_v)
