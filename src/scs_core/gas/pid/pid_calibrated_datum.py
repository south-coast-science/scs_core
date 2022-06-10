"""
Created on 24 May 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The PIDCalibratedDatum is a normalised PID output voltage. Its vCal field represents the calibrated weV.

example document:
{"weV": 0.39519, "aeV": 0.39963, "weC": 0.00627, "cnc": 61.9, "vCal": -9.801, "xCal": -12.601}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum

from scs_core.gas.pid.pid_calib import PIDCalib
from scs_core.gas.pid.pid_datum import PIDDatum


# --------------------------------------------------------------------------------------------------------------------

class PIDCalibrator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib: PIDCalib):
        """
        Constructor
        """
        self.__pid_elc_v = round(calib.pid_elc_mv / 1000.0, 3)                  # zero offset in Volts
        self.__pid_sens_v = round(calib.pid_sens_mv_ppm / 1000000.0, 6)         # sensitivity in Volts / ppb


    # ----------------------------------------------------------------------------------------------------------------

    def calibrate(self, datum):
        v_cal = self.__calibrate(datum, self.pid_sens_v)

        return PIDCalibratedDatum(datum.we_v, datum.we_c, datum.cnc, v_cal)


    def __calibrate(self, datum, pid_sens_v):
        if pid_sens_v is None:
            return None

        # zero offset...
        pid_v_zero_cal = datum.we_v - self.pid_elc_v

        # gain...
        return pid_v_zero_cal / pid_sens_v


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pid_elc_v(self):
        return self.__pid_elc_v


    @property
    def pid_sens_v(self):
        return self.__pid_sens_v


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalibrator:{pid_elc_v:%s, pid_sens_v:%s}" % (self.pid_elc_v, self.pid_sens_v)


# --------------------------------------------------------------------------------------------------------------------

class PIDCalibratedDatum(PIDDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        we_v = jdict.get('weV')
        we_c = jdict.get('weC')
        cnc = jdict.get('cnc')

        v_cal = jdict.get('vCal')

        return cls(we_v, we_c, cnc, v_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, we_c, cnc, v_cal):
        """
        Constructor
        """
        super().__init__(we_v, we_c=we_c, cnc=cnc)

        self.__v_cal = Datum.float(v_cal, 3)                        # calibrated ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['weC'] = self.we_c                                # may be None
        jdict['cnc'] = self.cnc                                 # may be None

        if self.v_cal is not None:
            jdict['vCal'] = self.v_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def v_cal(self):
        return self.__v_cal


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalibratedDatum:{we_v:%s, we_c:%s, cnc:%s, v_cal:%s}" % \
               (self.we_v, self.we_c, self.cnc, self.v_cal)
