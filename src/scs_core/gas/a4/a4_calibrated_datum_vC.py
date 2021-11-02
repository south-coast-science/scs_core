"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The A4CalibratedDatum is designed to provide a model training data set that encapsulates the calibration of the
electrochemical sensor - cal_x_v is only relevant to sensors with NO2 cross-sensitivity.
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.datetime import LocalizedDatetime

from scs_core.gas.a4.a4_calib import A4Calib
from scs_core.gas.a4.a4_datum import A4Datum


# TODO: return to this modelling technique using calib-age, when we have a wider range of calib-age training data?
# --------------------------------------------------------------------------------------------------------------------

class A4Calibrator(object):
    """
    classdocs
    """

    @classmethod
    def construct(cls, calib: A4Calib, era_start: LocalizedDatetime, era_end: LocalizedDatetime):
        era_length = era_end - era_start
        era_midpoint = era_end - (era_length / 2)

        return cls(calib, era_midpoint.timestamp())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib: A4Calib, era_midpoint):
        """
        Constructor
        """
        self.__calib = calib                                                # A4Calib

        self.__we_elc_v = calib.we_elc_mv / 1000.0
        self.__ae_elc_v = calib.ae_elc_mv / 1000.0

        self.__we_sens_v = calib.we_sens_mv / 1000.0

        self.__we_no2_x_sens_v = None if calib.we_no2_x_sens_mv is None else calib.we_no2_x_sens_mv / 1000.0

        self.__era_midpoint = int(era_midpoint)


    # ----------------------------------------------------------------------------------------------------------------

    def train(self, datetime: LocalizedDatetime, datum, no2_cnc=None):
        timestamp = int(datetime.timestamp())
        cursor = timestamp - self.__era_midpoint

        return self.calibrate(datum, no2_cnc=no2_cnc, cursor=cursor)


    def calibrate(self, datum, no2_cnc=None, cursor=0):
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
                                 we_v_zero_cal, ae_v_zero_cal, v_cal, v_x_cal, cursor)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calibrator:{calib:%s, era_midpoint:%s}" % (self.__calib, self.__era_midpoint)


# --------------------------------------------------------------------------------------------------------------------

class A4CalibratedDatum(A4Datum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c, cnc, we_v_zero_cal, ae_v_zero_cal, v_cal, v_x_cal, cursor):
        """
        Constructor
        """
        super().__init__(we_v, ae_v, we_c, cnc)

        self.__we_v_zero_cal = Datum.float(we_v_zero_cal, 6)        # zero-offset-corrected WE voltage
        self.__ae_v_zero_cal = Datum.float(ae_v_zero_cal, 6)        # zero-offset-corrected AE voltage

        self.__v_cal = Datum.float(v_cal, 6)                        # calibrated voltage
        self.__v_x_cal = Datum.float(v_x_cal, 9)                    # calibrated cross-sensitivity voltage

        self.__cursor = int(cursor)                                 # timestamp relative to era midpoint


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

        jdict['cursor'] = self.cursor

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


    @property
    def cursor(self):
        return self.__cursor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4CalibratedDatum(vC):{we_v:%s, ae_v:%s, we_c:%s, cnc:%s, " \
               "we_v_zero_cal:%s, ae_v_zero_cal:%s, v_cal:%s, v_x_cal:%s, cursor:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc,
                self.we_v_zero_cal, self.ae_v_zero_cal, self.v_cal, self.v_x_cal, self.cursor)
