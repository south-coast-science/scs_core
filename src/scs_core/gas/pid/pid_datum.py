"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PIDDatum(JSONable):
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

        return cls(we_v, we_c, cnc)


    @classmethod
    def construct(cls, calib, baseline, tc, temp, we_v):
        if calib is None or tc is None:
            return PIDDatum(we_v)

        # weC...
        we_c = cls.__we_c(calib, tc, temp, we_v)

        if we_c is None:
            return PIDDatum(we_v)

        # cnc...
        cnc = cls.__cnc(calib, we_c)

        baselined_cnc = cnc + baseline.offset               # a positive offset causes the value to be raised

        return cls(we_v, we_c, baselined_cnc)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __we_c(cls, calib, tc, temp, we_v):
        """
        Compute weC from sensor temperature compensation of weV
        """
        offset_v = calib.pid_elc_mv / 1000.0

        response_v = we_v - offset_v                    # remove electronic zero
        response_c = tc.correct(temp, response_v)       # correct the response component

        if response_c is None:
            return None

        we_c = response_c + offset_v                    # replace electronic zero

        return we_c


    @classmethod
    def __cnc(cls, calib, we_c):
        """
        Compute cnc from weC
        """
        if we_c is None:
            return None

        offset_v = calib.pid_elc_mv / 1000.0

        response_c = we_c - offset_v                    # remove electronic zero
        cnc = response_c / calib.pid_sens_v_ppb         # units are Volts / ppb

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_v = Datum.float(we_v, 5)              # uncorrected working electrode output      Volts

        self.__we_c = Datum.float(we_c, 5)              # corrected working electrode voltage       Volts
        self.__cnc = Datum.float(cnc, 1)                # gas concentration                         ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v

        jdict['weC'] = self.we_c                        # may be None
        jdict['cnc'] = self.cnc                         # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_v(self):
        return self.__we_v


    @property
    def we_c(self):
        return self.__we_c


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDDatum:{we_v:%0.6f, we_c:%s, cnc:%s}" % (self.we_v, self.we_c, self.cnc)
