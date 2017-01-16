"""
Created on 30 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MonitorResponse(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message, error=None):
        """
        Constructor
        """
        self.__message = message
        self.__error = error


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['msg'] = self.message
        jdict['err'] = self.error

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def message(self):
        return self.__message


    @property
    def error(self):
        return self.__error


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MonitorResponse:{message:%s, error:%s}" % (self.message, self.error)
