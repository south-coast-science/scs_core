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

    def __init__(self, we_t, cnc=None):
        """
        Constructor
        """
        self.__we_t = Datum.float(we_t, 6)      # uncorrected working electrode output         Volts
        self.__cnc = cnc                        # gas concentration                            ppb (d)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weT'] = self.we_t

        jdict['cnc'] = self.cnc                 # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_t(self):
        return self.__we_t


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDDatum:{we_t:%0.6f, cnc:%s}" % (self.we_t, self.cnc)
