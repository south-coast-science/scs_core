"""
Created on 18 Sep 2016

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

    def __init__(self, temp, voltage, cnc, cnc_igl):
        """
        Constructor
        """
        self.__temp = Datum.float(temp, 1)              # temperature                       ºC
        self.__voltage = Datum.int(voltage)             # voltage                           mV
        self.__cnc = Datum.float(cnc, 1)                # concentration                     ppm
        self.__cnc_igl = Datum.float(cnc_igl, 1)        # concentration (ideal gas law)     ppm


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tmp'] = self.temp
        jdict['v'] = self.voltage
        jdict['cnc'] = self.cnc
        jdict['cnc-igl'] = self.cnc_igl

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def temp(self):
        return self.__temp


    @property
    def voltage(self):
        return self.__voltage


    @property
    def cnc(self):
        return self.__cnc


    @property
    def cnc_igl(self):
        return self.__cnc_igl


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRDatum:{temp:%0.1f, voltage:%d, cnc:%0.1f, cnc_igl:%0.1f}" % \
               (self.temp, self.voltage, self.cnc, self.cnc_igl)
