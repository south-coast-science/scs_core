"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV Qualifiers

example:
{"code": "88502", "type": "Acceptable PM2.5 AQI & Mass", "type_description": "105"}
"""

import json
import os

from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Qualifier(JSONable):
    """
    classdocs
    """

    __qualifiers = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/specifications/qualifiers.csv"

        reader = CSVReader(filename=filename, cast=False)

        try:
            for row in reader.rows:
                qualifier = cls.construct_from_jdict(json.loads(row))
                cls.__qualifiers[qualifier.code] = qualifier

        finally:
            reader.close()


    @classmethod
    def qualifiers(cls):
        for qualifier in cls.__qualifiers.values():
            yield qualifier


    @classmethod
    def find_by_code(cls, code):
        if code not in cls.__qualifiers:
            return None

        return cls.__qualifiers[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        description = jdict.get('description')

        type_code = jdict.get('type-code')
        type_description = str(jdict.get('type-description'))


        return Qualifier(code, description, type_code, type_description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, description, type_code, type_description):
        """
        Constructor
        """
        self.__code = code                                      # string
        self.__description = description                        # string

        self.__type_code = type_code                            # string
        self.__type_description = type_description              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['description'] = self.description

        jdict['type-code'] = self.type_code
        jdict['type-description'] = self.type_description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def description(self):
        return self.__description


    @property
    def type_code(self):
        return self.__type_code


    @property
    def type_description(self):
        return self.__type_description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Qualifier:{code:%s, description:%s, type_code:%s, type_description:%s}" %  \
               (self.code, self.description, self.type_code, self.type_description)
