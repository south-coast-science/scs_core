"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# TODO: clean up PID data interpretation

# --------------------------------------------------------------------------------------------------------------------

class PIDDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, calib, baseline, tc, temp, we_v):
        if calib is None or tc is None:
            return PIDDatum(we_v)

        # print("PIDDatum.construct: calib:%s baseline:%s tc:%s temp:%.1f we_v:%f" % (calib, baseline, tc, temp, we_v),
        #       file=sys.stderr)
        # print("-", file=sys.stderr)

        # weC...
        we_c = cls.__we_c(calib, tc, temp, we_v)

        if we_c is None:
            return PIDDatum(we_v)

        # cnc...
        cnc = cls.__cnc(calib.pid_elc_mv, calib.pid_sens_mv, we_c)

        baselined_cnc = cnc + baseline.offset

        # print("PIDDatum.construct: baselined_cnc:%s" % baselined_cnc, file=sys.stderr)
        # print("-", file=sys.stderr)

        return PIDDatum(we_v, we_c, baselined_cnc)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __we_c(cls, calib, tc, temp, we_v):
        """
        Compute weC from sensor temperature compensation of weV
        """
        # we_t = we_v - (float(calib.pid_elc_mv) / 1000.0)        # remove electronic zero

        we_c = tc.correct(temp, we_v)

        # print("PIDDatum.__we_c: we_v:%f we_t:%f we_c:%s" % (we_v, we_v, we_c), file=sys.stderr)

        return we_c


    @classmethod
    def __cnc(cls, pid_elc_mv, sens_mv, we_c):
        """
        Compute cnc from weC
        """
        if we_c is None:
            return None

        # cnc = (we_c / (sens_mv / 1000.0)) * 1000.0     # to get ppb
        cnc = (we_c - (pid_elc_mv / 1000.0)) / sens_mv          # * 1000.0     # to get ppb

        # print("PIDDatum__cnc: we_c:%s pid_elc_mv:%s cnc:%f" % (we_c, pid_elc_mv, cnc), file=sys.stderr)

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_v = Datum.float(we_v, 6)          # uncorrected working electrode output      Volts

        self.__we_c = Datum.float(we_c, 6)          # corrected working electrode voltage       Volts
        self.__cnc = Datum.float(cnc, 1)            # gas concentration                         ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v

        jdict['weC'] = self.we_c                    # may be None
        jdict['cnc'] = self.cnc                     # may be None

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
