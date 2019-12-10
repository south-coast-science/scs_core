"""
Created on 7 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Datum for Integrated Electrochem Interface (ISI)
"""

from collections import OrderedDict

from scs_core.data.datum import Format
from scs_core.data.json import JSONable


# TODO: rename as Gas Sensor Interface Datum

# --------------------------------------------------------------------------------------------------------------------

class ISIDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *sns):
        """
        Constructor
        """
        self.__sns = OrderedDict(sns)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['src'] = 'ISI'
        jdict['sns'] = self.sns

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sns(self):
        return self.__sns


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISIDatum:{sns:%s}" % Format.collection(self.sns)
