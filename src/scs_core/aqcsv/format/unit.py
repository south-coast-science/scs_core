"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"code": "083", "description": "Cubic meters/minute STP"}
"""

import json
import os

from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Unit(JSONable):
    """
    classdocs
    """

    __units = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/codes/units.csv"

        reader = CSVReader(filename, cast=False)

        try:
            for row in reader.rows:
                unit = cls.construct_from_jdict(json.loads(row))
                cls.__units[unit.code] = unit

        finally:
            reader.close()


    @classmethod
    def units(cls):
        for unit in cls.__units.values():
            yield unit


    @classmethod
    def find_by_code(cls, code):
        if code not in cls.__units:
            return None

        return cls.__units[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        description = jdict.get('description')

        return Unit(code, description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, description):
        """
        Constructor
        """
        self.__code = code                                  # string
        self.__description = description                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['description'] = self.description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Unit:{code:%s, description:%s}" %  (self.code, self.description)
