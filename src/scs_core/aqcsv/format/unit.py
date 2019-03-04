"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"code": 788, "description": "Tunisia", "unit_code": "TUN"}

https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
"""

import json
import os

from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Parameter(JSONable):
    """
    classdocs
    """

    __parameters = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/codes/parameters.csv"

        reader = CSVReader(filename, cast=False)

        try:
            for row in reader.rows:
                parameter = cls.construct_from_jdict(json.loads(row))
                cls.__parameters[parameter.code] = parameter

        finally:
            reader.close()


    @classmethod
    def parameters(cls):
        for code in cls.__parameters.values():
            yield code


    @classmethod
    def find_by_code(cls, code):
        if code not in cls.__parameters:
            return None

        return cls.__parameters[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        description = jdict.get('description')
        unit_code = str(jdict.get('unit_code'))


        return Parameter(code, description, unit_code)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, description, unit_code):
        """
        Constructor
        """
        self.__code = code                                  # string
        self.__description = description                    # string
        self.__unit_code = unit_code                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['description'] = self.description
        jdict['unit_code'] = self.unit_code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def description(self):
        return self.__description


    @property
    def unit_code(self):
        return self.__unit_code


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Parameter:{code:%s, description:%s, unit_code:%s}" %  (self.code, self.description, self.unit_code)
