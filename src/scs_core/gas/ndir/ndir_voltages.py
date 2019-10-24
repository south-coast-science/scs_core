"""
Created on 24 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRVoltages(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        ref = jdict.get('ref')
        act = jdict.get('act')
        therm = jdict.get('therm')

        return NDIRVoltages(ref, act, therm)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ref, act, therm):
        """
        Constructor
        """
        self.__ref = Datum.float(ref, 6)                # pile_ref_amplitude        Volts
        self.__act = Datum.float(act, 6)                # pile_act_amplitude        Volts
        self.__therm = Datum.float(therm, 6)            # thermistor_average        Volts


    def __eq__(self, other):
        try:
            return self.ref == other.ref and self.act == other.act and self.therm == other.therm

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------
    # Support for averaging...

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)

        ref = self.ref + other.ref
        act = self.act + other.act
        therm = self.therm + other.therm

        return NDIRVoltages(ref, act, therm)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        ref = self.ref / other
        act = None if self.act is None else self.act / other
        therm = None if self.therm is None else self.therm / other

        return NDIRVoltages(ref, act, therm)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ref'] = self.ref
        jdict['act'] = self.act
        jdict['therm'] = self.therm

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ref(self):
        return self.__ref


    @property
    def act(self):
        return self.__act


    @property
    def therm(self):
        return self.__therm


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRVoltages:{ref:%s, act:%s, therm:%s}" % (self.ref, self.act, self.therm)
