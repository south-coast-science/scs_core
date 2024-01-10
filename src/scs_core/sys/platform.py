"""
Created on 28 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"rel": "4.19.103-bone47", "vers": "#1buster PREEMPT Thu Feb 20 17:40:41 UTC 2020"}

https://docs.python.org/3/library/platform.html
"""

import platform

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

        release = jdict.get('rel')

        return cls(release)


    @classmethod
    def construct(cls):
        uname = platform.uname()

        return cls(uname.release)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, release):
        """
        Constructor
        """
        self.__release = release                          # string


    def __eq__(self, other):
        try:
            return self.release == other.release

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rel'] = self.release

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def release(self):
        return self.__release


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PlatformSummary:{release:%s}" %  self.release
