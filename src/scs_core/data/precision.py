"""
Created on 12 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

class Precision(object):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, digits=None):
        """
        Constructor
        """
        self.__digits = digits            # int


    # ----------------------------------------------------------------------------------------------------------------

    def widen(self, value):
        digits = Datum.precision(value)

        if digits is None:
            return

        if self.__digits is None or digits > self.__digits:
            self.__digits = digits


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def digits(self):
        return self.__digits


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Precision:{digits:%s}" % self.digits
