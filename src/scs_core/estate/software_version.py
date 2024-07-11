"""
Created on 28 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
1.23
3.2.27
03.02.27

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

        match = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?', jdict)

        if not match:
            raise ValueError(jdict)

        return cls([int(part) for part in match.groups() if part is not None])


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
            return self.as_json(sortable=True) == other.as_json(sortable=True)

        except (TypeError, AttributeError):
            return False


    def __gt__(self, other):
        return self.as_json(sortable=True) > other.as_json(sortable=True)


    def __lt__(self, other):
        return self.as_json(sortable=True) < other.as_json(sortable=True)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, sortable=False, **kwargs):
        return '.'.join(["%02d" % part if sortable else "%d" % part for part in self.__parts])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def parts(self):
        return self.__parts


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SoftwareVersion:{%s}" % self.parts
