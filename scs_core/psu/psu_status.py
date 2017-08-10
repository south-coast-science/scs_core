"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"p-rst": false, "w-rst": false, "batt-flt": false, "host-3v3": 3.4, "pwr-in": 9.6, "prot-batt": 5.0}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        power_reset = jdict.get('p-rst')
        watchdog_reset = jdict.get('w-rst')

        battery_fault = jdict.get('batt-flt')

        host_3v3 = jdict.get('host-3v3')
        power_in = jdict.get('pwr-in')
        prot_batt = jdict.get('prot-batt')

        return PSUStatus(power_reset, watchdog_reset, battery_fault, host_3v3, power_in, prot_batt)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_reset, watchdog_reset, battery_fault, host_3v3, power_in, prot_batt):
        """
        Constructor
        """
        self.__power_reset = power_reset                        # restart because host was powered down     bool
        self.__watchdog_reset = watchdog_reset                  # restart because of watchdog timeout       bool

        self.__battery_fault = battery_fault                    # battery fault                             bool

        self.__host_3v3 = Datum.float(host_3v3, 1)              # host 3V3 voltage                          float
        self.__power_in = Datum.float(power_in, 1)              # PSU input voltage                         float
        self.__prot_batt = Datum.float(prot_batt, 1)            # battery voltage                           float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['p-rst'] = self.power_reset
        jdict['w-rst'] = self.watchdog_reset

        jdict['batt-flt'] = self.battery_fault

        jdict['host-3v3'] = self.host_3v3
        jdict['pwr-in'] = self.power_in
        jdict['prot-batt'] = self.prot_batt

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power_reset(self):
        return self.__power_reset


    @property
    def watchdog_reset(self):
        return self.__watchdog_reset


    @property
    def battery_fault(self):
        return self.__battery_fault


    @property
    def host_3v3(self):
        return self.__host_3v3


    @property
    def power_in(self):
        return self.__power_in


    @property
    def prot_batt(self):
        return self.__prot_batt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{power_reset:%s, watchdog_reset:%s, battery_fault:%s, " \
               "host_3v3:%s, power_in:%s, prot_batt:%s}" \
               % (self.power_reset, self.watchdog_reset, self.battery_fault,
                  self.host_3v3, self.power_in, self.prot_batt)
