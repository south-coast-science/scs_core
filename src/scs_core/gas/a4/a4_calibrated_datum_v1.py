"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The A4CalibratedDatum is designed to provide a model training data set that encapsulates the calibration of the
electrochemical sensor - the fields we_v_cal, ae_v_zero_cal and cal_x_v have no meaning beyond this.
cal_x_v is only relevant to sensors with NO2 cross-sensitivity.
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

        self.__we_elc_v = calib.we_elc_mv / 1000.0
        self.__ae_elc_v = calib.ae_elc_mv / 1000.0

        self.__we_sens_v = calib.we_sens_mv / 1000.0

        self.__we_no2_x_sens_v = None if calib.we_no2_x_sens_mv is None else calib.we_no2_x_sens_mv / 1000.0


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum, no2_cnc=None):
        # zero offset...
        we_v_zero_cal = datum.we_v - self.__we_elc_v
        ae_v_zero_cal = datum.ae_v - self.__ae_elc_v

        # gain...
        we_v_cal = we_v_zero_cal / self.__we_sens_v

        # cross sensitivity...
        cal_x_v = None if no2_cnc is None else no2_cnc * self.__we_no2_x_sens_v

        return A4CalibratedDatum(datum.we_v, datum.ae_v, datum.we_c, datum.cnc, we_v_cal, ae_v_zero_cal, cal_x_v)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calibrator:{calib:%s}" % self.__calib


# --------------------------------------------------------------------------------------------------------------------

class A4CalibratedDatum(A4Datum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, we_v_cal, ae_v_cal, cal_x_v):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__we_v_cal = Datum.float(we_v_cal, 6)              # calibrated WE voltage
        self.__ae_v_cal = Datum.float(ae_v_cal, 6)              # calibrated AE voltage

        self.__cal_x_v = Datum.float(cal_x_v, 9)                # calibrated cross-sensitivity voltage


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                            # may be None
        jdict['cnc'] = self.cnc                             # may be None

        jdict['weVCal'] = self.we_v_cal
        jdict['aeVCal'] = self.ae_v_cal

        if self.cal_x_v is not None:
            jdict['calXV'] = self.cal_x_v

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_v_cal(self):
        return self.__we_v_cal


    @property
    def ae_v_cal(self):
        return self.__ae_v_cal


    @property
    def cal_x_v(self):
        return self.__cal_x_v


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum(v1):{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, we_v_cal:%s, ae_v_cal:%s, cal_x_v:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc, self.we_v_cal, self.ae_v_cal, self.cal_x_v)
