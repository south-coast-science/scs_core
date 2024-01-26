"""
Created on 28 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
3.2.27

https://en.wikipedia.org/wiki/Software_versioning
"""

import re

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SoftwareVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        match = re.match(r'^(\d+).(\d+).(\d+)', jdict)

        if not match:
            raise ValueError(jdict)

        return cls([int(part) for part in match.groups()])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, parts):
        """
        Constructor
        """
        self.__parts = parts                                # list of int


    def __len__(self):
        return len(self.__parts)


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for i in range(len(self)):
                if self.__parts[i] != other.__parts[i]:
                    return False

            return True

        except (TypeError, AttributeError):
            return False


    def __gt__(self, other):
        if len(self) != len(other):
            raise ValueError(other)

        for i in range(len(self)):
            if self.__parts[i] > other.__parts[i]:
                return True

            if self.__parts[i] < other.__parts[i]:
                return False

        return False


    def __lt__(self, other):
        if len(self) != len(other):
            raise ValueError(other)

        for i in range(len(self)):
            if self.__parts[i] < other.__parts[i]:
                return True

            if self.__parts[i] > other.__parts[i]:
                return False


        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return '.'.join([str(part) for part in self.__parts])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def parts(self):
        return self.__parts


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SoftwareVersion:{parts:%s}" % self.parts
