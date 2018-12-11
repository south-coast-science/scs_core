"""
Created on 11 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A leaf node of a JSON document, appropriate for numeric processing. This class be used to preserve the precision of
the original value.
"""

from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

class Leaf(object):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, precision=None):
        """
        Constructor
        """
        self.__path = path                      # string
        self.__precision = precision            # int


    # ----------------------------------------------------------------------------------------------------------------

    def widen_precision(self, value):
        precision = Datum.precision(value)

        if precision is None:
                return

        if self.__precision is None or precision > self.__precision:
            self.__precision = precision


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def precision(self):
        return self.__precision


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Leaf:{path:%s, precision:%s}" % (self.path, self.precision)
