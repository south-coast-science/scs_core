"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV Measurement performance characteristics

example:
{"code": "88502", "definition": "Acceptable PM2.5 AQI & Mass", "description": "105"}
"""

import json
import os

from collections import OrderedDict

from scs_core.aqcsv.format.unit import Unit
from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MPC(JSONable):
    """
    classdocs
    """

    __mcps = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        Unit.load()

        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/specifications/mcps.csv"

        reader = CSVReader(filename=filename, cast=False)

        try:
            for row in reader.rows:
                parameter = cls.construct_from_jdict(json.loads(row))
                cls.__mcps[parameter.code] = parameter

        finally:
            reader.close()


    @classmethod
    def mcps(cls):
        for code in cls.__mcps.values():
            yield code


    @classmethod
    def find_by_code(cls, code):
        if code not in cls.__mcps:
            return None

        return cls.__mcps[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        abbreviation = jdict.get('abbreviation')
        definition = jdict.get('definition')
        description = str(jdict.get('description'))


        return MPC(code, abbreviation, definition, description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, abbreviation, definition, description):
        """
        Constructor
        """
        self.__code = code                                      # string
        self.__abbreviation = abbreviation                      # string
        self.__definition = definition                          # string
        self.__description = description                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['abbreviation'] = self.abbreviation
        jdict['definition'] = self.definition
        jdict['description'] = self.description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def abbreviation(self):
        return self.__abbreviation


    @property
    def definition(self):
        return self.__definition


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPC:{code:%s, abbreviation:%s, definition:%s, description:%s}" %  \
               (self.code, self.abbreviation, self.definition, self.description)
