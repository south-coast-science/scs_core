"""
Created on 28 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"os": "10.13", "kernel": "6.1.77-bone30"}

https://docs.python.org/3/library/platform.html
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PlatformSummary(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        os = jdict.get('os')
        kernel = jdict.get('kernel')

        return cls(os, kernel)


    @classmethod
    def construct(cls, manager):
        return cls(manager.os_release(), manager.kernel_release())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, os, kernel):
        """
        Constructor
        """
        self.__os = os                                  # string
        self.__kernel = kernel                          # string


    def __eq__(self, other):
        try:
            return self.os == other.os and self.kernel == other.kernel

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['os'] = self.os
        jdict['kernel'] = self.kernel

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def os(self):
        return self.__os


    @property
    def kernel(self):
        return self.__kernel


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PlatformSummary:{os:%s, kernel:%s}" %  (self.os, self.kernel)
