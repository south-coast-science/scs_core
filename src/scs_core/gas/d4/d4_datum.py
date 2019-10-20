"""
Created on 18 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense D4 electrochemical sensor

Alphasense Application Note AAN 803-02
AAN 803-02 070916_DRAFT03.doc
"""

# import sys

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class D4Datum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, calib, baseline, tc, temp, we_v):
        if calib is None or tc is None:
            return D4Datum(we_v)

        # print("D4Datum: calib:%s baseline:%s tc:%s temp:%f we_v:%f x_sens_sample:%s" %
        #       (calib, baseline, tc, temp, we_v, x_sens_sample), file=sys.stderr)

        # weC...
        we_c = cls.__we_c(calib, tc, temp, we_v)

        if we_c is None:
            return D4Datum(we_v)

        # cnc...
        cnc = cls.__cnc(calib.we_sens_mv, we_c)

        baselined_cnc = cnc + baseline.offset

        return D4Datum(we_v, we_c, baselined_cnc)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __we_c(cls, calib, tc, temp, we_v):
        """
        Compute weC from sensor temperature compensation of weV, aeV
        """
        we_t = we_v - (calib.we_elc_mv / 1000.0)        # remove electronic we zero

        we_c = tc.correct(calib, temp, we_t)

        # print("D4Datum__we_c: we_t:%f we_c:%s" % (we_t, we_c), file=sys.stderr)

        return we_c


    @classmethod
    def __cnc(cls, sens_mv, we_c):
        """
        Compute cnc from weC (using primary sensitivity)
        """
        if we_c is None:
            return None

        cnc = we_c / (sens_mv / 1000.0)

        # print("D4Datum__cnc: we_c:%s cnc:%f" % (we_c, cnc), file=sys.stderr)

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_v = Datum.float(we_v, 5)        # uncorrected working electrode voltage       Volts

        self.__we_c = Datum.float(we_c, 5)        # corrected working electrode voltage         Volts
        self.__cnc = Datum.float(cnc, 1)          # gas concentration                           ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v

        jdict['weC'] = self.we_c                 # may be None
        jdict['cnc'] = self.cnc                  # may be None

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
        we_v = None if self.we_v is None else round(float(self.we_v), 5)
        we_c = None if self.we_c is None else round(float(self.we_c), 5)
        cnc = None if self.cnc is None else round(float(self.cnc), 5)

        return "D4Datum:{we_v:%s, we_c:%s, cnc:%s}" % (we_v, we_c, cnc)
