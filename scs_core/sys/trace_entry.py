"""
Created on 9 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TraceEntry(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, text):
        lines = [line.strip() for line in text.splitlines()]

        location = lines[0]
        statement = lines[1] if len(lines) > 1 else None

        return TraceEntry(location, statement)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location, statement):
        """
        Constructor
        """
        self.__location = location
        self.__statement = statement


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['loc'] = self.location
        jdict['stat'] = self.statement

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location(self):
        return self.__location


    @property
    def statement(self):
        return self.__statement


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TraceEntry:{location:%s, statement:%s}" % (self.location, self.statement)
