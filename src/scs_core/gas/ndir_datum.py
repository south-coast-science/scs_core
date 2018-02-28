"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        temp = jdict.get('tmp')
        cnc = jdict.get('cnc-raw')
        cnc_igl = jdict.get('cnc')

        return NDIRDatum(temp, cnc, cnc_igl)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cnc, cnc_igl, temp):
        """
        Constructor
        """
        self.__temp = Datum.float(temp, 1)              # temperature                               ºC
        self.__cnc = Datum.float(cnc, 1)                # concentration                             ppm
        self.__cnc_igl = Datum.float(cnc_igl, 1)        # concentration (ideal gas law corrected)   ppm


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.temp != other.temp:
            return False

        if self.cnc != other.cnc:
            return False

        if self.cnc_igl != other.cnc_igl:
            return False

        return True


    def __add__(self, other):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tmp'] = self.temp
        jdict['cnc-raw'] = self.cnc
        jdict['cnc'] = self.cnc_igl

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def temp(self):
        return self.__temp


    @property
    def cnc(self):
        return self.__cnc


    @property
    def cnc_igl(self):
        return self.__cnc_igl


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRDatum:{temp:%0.1f, cnc:%0.1f, cnc_igl:%0.1f}" % \
               (self.temp, self.cnc, self.cnc_igl)
