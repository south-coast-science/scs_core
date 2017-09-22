"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

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
    def construct(cls, calib, baseline, tc, temp, we_v):
        if calib is None or tc is None:
            return PIDDatum(we_v)

        print("PIDDatum: calib:%s baseline:%s tc:%s temp:%f we_v:%f" %
              (calib, baseline, tc, temp, we_v), file=sys.stderr)

        # weC...
        we_c = cls.__we_c(calib, tc, temp, we_v)

        if we_c is None:
            return PIDDatum(we_v)

        # cnc...
        cnc = cls.__cnc(calib.we_sens_mv, we_c)

        baselined_cnc = cnc + baseline.offset

        return PIDDatum(we_v, we_c, baselined_cnc)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_t, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_t = Datum.float(we_t, 6)          # uncorrected working electrode output      Volts

        self.__we_c = Datum.float(we_c, 6)          # corrected working electrode voltage       Volts
        self.__cnc = Datum.float(cnc, 1)            # gas concentration                         ppb


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __we_c(cls, calib, tc, temp, we_v):
        """
        Compute weC from sensor temperature compensation of weV
        """
        we_t = we_v - (float(calib.we_elc_mv) / 1000.0)

        we_c = tc.correct(calib, temp, we_t)

        print("PIDDatum__we_c: we_t:%f we_c:%s" % (we_t, we_c), file=sys.stderr)

        return we_c


    @classmethod
    def __cnc(cls, sens_mv, we_c):
        """
        Compute cnc from weC
        """
        if we_c is None:
            return None

        cnc = (we_c * 1000.0) / sens_mv

        print("PIDDatum__cnc: we_c:%s cnc:%f" % (we_c, cnc), file=sys.stderr)

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weT'] = self.we_t

        jdict['weC'] = self.we_c                    # may be None
        jdict['cnc'] = self.cnc                     # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_t(self):
        return self.__we_t


    @property
    def we_c(self):
        return self.__we_c


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDDatum:{we_t:%0.6f, we_c:%s, cnc:%s}" % (self.we_t, self.we_c, self.cnc)
