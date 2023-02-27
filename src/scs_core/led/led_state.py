"""
Created on 5 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"colour0": "R", "colour1": "G"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.led.led import LED


# --------------------------------------------------------------------------------------------------------------------

class LEDState(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        colour0 = jdict.get('colour0')
        colour1 = jdict.get('colour1')

        return LEDState(colour0, colour1)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, colour0, colour1):
        """
        Constructor
        """
        self.__colour0 = colour0                    # colour - short period
        self.__colour1 = colour1                    # colour - long period


    def __eq__(self, other):
        try:
            return self.__colour0 == other.__colour0 and self.__colour1 == other.__colour1

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return LED.is_valid_colour(self.colour0) and LED.is_valid_colour(self.colour1)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['colour0'] = self.colour0
        jdict['colour1'] = self.colour1

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def colour0(self):
        return self.__colour0


    @property
    def colour1(self):
        return self.__colour1


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LEDState:{colour0:%s, colour1:%s}" % (self.colour0, self.colour1)
