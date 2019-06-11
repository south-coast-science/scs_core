"""
Created on 7 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class IEIDatum(JSONable):
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

        jdict['src'] = 'IEI'
        jdict['sns'] = self.sns

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sns(self):
        return self.__sns


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sns = '{' + ', '.join(str(key) + ':' + str(self.sns[key]) for key in self.sns) + '}'

        return "IEIDatum:{sns:%s}" % sns
