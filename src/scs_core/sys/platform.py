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
        version = jdict.get('vers')

        return cls(release, version)


    @classmethod
    def construct(cls):
        uname = platform.uname()

        return cls(uname.release, uname.version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, release, version):
        """
        Constructor
        """
        self.__release = release                          # string
        self.__version = version                          # string


    def __eq__(self, other):
        try:
            return self.release == other.release and self.version == other.version

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rel'] = self.release
        jdict['vers'] = self.version

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def release(self):
        return self.__release


    @property
    def version(self):
        return self.__version


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PlatformSummary:{release:%s, version:%s}" %  \
               (self.release, self.version)
