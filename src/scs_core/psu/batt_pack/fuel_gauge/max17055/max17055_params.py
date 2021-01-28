"""
Created on 3 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Values stored here shall be in their raw (16-bit unsigned int) form.

https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/6/6365.html

Document example:
{"calibrated-on": "2021-01-02T09:34:48Z",
"r-comp-0": 201, "temp-co": 9278, "full-cap-rep": 1790, "full-cap-nom": 4896, "cycles": 210}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Max17055Params(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "max17055_params.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        r_comp_0 = jdict.get('r-comp-0')
        temp_co = jdict.get('temp-co')
        full_cap_rep = jdict.get('full-cap-rep')
        full_cap_nom = jdict.get('full-cap-nom')

        cycles = jdict.get('cycles')

        return cls(calibrated_on, r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on            # unsigned int

        self.__r_comp_0 = r_comp_0                      # unsigned int
        self.__temp_co = temp_co                        # unsigned int
        self.__full_cap_rep = full_cap_rep              # unsigned int
        self.__full_cap_nom = full_cap_nom              # unsigned int

        self.__cycles = Datum.int(cycles)               # unsigned int


    def __eq__(self, other):                            # ignore calibrated_on, cycles
        return self.r_comp_0 == other.r_comp_0 and \
               self.temp_co == other.temp_co and \
               self.full_cap_rep == other.full_cap_rep and \
               self.full_cap_nom == other.full_cap_nom


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        if not self.__calibrated_on:
            self.__calibrated_on = LocalizedDatetime.now()

        super().save(manager, encryption_key=None)


    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = None if self.calibrated_on is None else self.calibrated_on.as_iso8601()

        jdict['r-comp-0'] = self.r_comp_0
        jdict['temp-co'] = self.temp_co
        jdict['full-cap-rep'] = self.full_cap_rep
        jdict['full-cap-nom'] = self.full_cap_nom

        jdict['cycles'] = self.cycles

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def r_comp_0(self):
        return self.__r_comp_0


    @property
    def temp_co(self):
        return self.__temp_co


    @property
    def full_cap_rep(self):
        return self.__full_cap_rep


    @property
    def full_cap_nom(self):
        return self.__full_cap_nom


    @property
    def cycles(self):
        return self.__cycles


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Max17055Params:{calibrated_on:%s, r_comp_0:%s, temp_co:%s, full_cap_rep:%s, full_cap_nom:%s, " \
               "cycles:%s}" % \
               (self.calibrated_on, self.r_comp_0, self.temp_co, self.full_cap_rep, self.full_cap_nom,
                self.cycles)
