"""
Created on 5 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MonitorError(JSONable):
    """
    classdocs
    """

    CODE_UNKNOWN_GRP =          'UNKNOWN_GRP'
    CODE_UNKNOWN_CMD =          'UNKNOWN_CMD'

    CODE_INVALID_PASSWORD =     'INVALID_PASSWORD'
    CODE_NO_SESSION =           'NO_SESSION'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, value=None):
        """
        Constructor
        """
        self.__code = code
        self.__value = value


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def value(self):
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MonitorError:{code:%s, value:%s}" % (self.code, self.value)
