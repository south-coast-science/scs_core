"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense Application Note AAN 803-02
AAN 803-02 070916_DRAFT03.doc
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class A4Datum(JSONable):
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

        return cls(we_v, ae_v, we_c, cnc)


    @classmethod
    def construct(cls, calib, baseline, tc, temp, we_v, ae_v, no2_cnc=None):
        if calib is None or tc is None:
            return A4Datum(we_v, ae_v)

        # print("A4Datum: calib:%s baseline:%s tc:%s temp:%f we_v:%f ae_v:%f x_sens_sample:%s" %
        #       (calib, baseline, tc, temp, we_v, ae_v, x_sens_sample), file=sys.stderr)

        # weC...
        we_c = cls.__we_c(calib, tc, temp, we_v, ae_v)

        if we_c is None:
            return A4Datum(we_v, ae_v)

        if no2_cnc:
            we_c -= cls.__reverse_we_c(calib.we_no2_x_sens_mv, no2_cnc)

        # cnc...
        cnc = cls.__cnc(calib.we_sens_mv, we_c)

        baselined_cnc = cnc + baseline.offset                # a positive offset causes the value to be raised

        return cls(we_v, ae_v, we_c, baselined_cnc)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __we_c(cls, calib, tc, temp, we_v, ae_v):
        """
        Compute weC from sensor temperature compensation of weV, aeV
        """
        we_t = we_v - (calib.we_elc_mv / 1000.0)        # remove electronic we zero
        ae_t = ae_v - (calib.ae_elc_mv / 1000.0)        # remove electronic ae zero

        we_c = tc.correct(calib, temp, we_t, ae_t)

        # print("A4Datum__we_c: we_t:%f ae_t:%f we_c:%s" % (we_t, ae_t, we_c), file=sys.stderr)

        return we_c


    @classmethod
    def __cnc(cls, sens_mv, we_c):
        """
        Compute cnc from weC (using primary sensitivity)
        """
        if we_c is None:
            return None

        cnc = we_c / (sens_mv / 1000.0)

        # print("A4Datum__cnc: we_c:%s cnc:%f" % (we_c, cnc), file=sys.stderr)

        return cnc


    @classmethod
    def __reverse_we_c(cls, sens_mv, cnc):      # TODO: don't use concentration - factor out baseline?
        """
        Compute weC from cnc (using cross-sensitivity)
        """
        we_c = (cnc * sens_mv) / 1000.0

        # print("__reverse_we_c: sens_mv:%s cnc:%f we_c:%s" % (sens_mv, cnc, we_c), file=sys.stderr)

        return we_c


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_v = Datum.float(we_v, 5)        # uncorrected working electrode voltage       Volts
        self.__ae_v = Datum.float(ae_v, 5)        # uncorrected auxiliary electrode voltage     Volts

        self.__we_c = Datum.float(we_c, 5)        # corrected working electrode voltage         Volts
        self.__cnc = Datum.float(cnc, 1)          # gas concentration                           ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                 # may be None
        jdict['cnc'] = self.cnc                  # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_v(self):
        return self.__we_v


    @property
    def ae_v(self):
        return self.__ae_v


    @property
    def we_c(self):
        return self.__we_c


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Datum:{we_v:%s, ae_v:%s, we_c:%s, cnc:%s}" % \
               (self.we_v, self.ae_v, self.we_c, self.cnc)
