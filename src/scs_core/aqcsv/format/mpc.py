"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV Measurement performance characteristics

example:
{"code": "3", "abbreviation": "XD", "definition": "Minimum Detectable Value",
"description": "The measure of inherent detection capability of a measurement process."}
"""

import json
import os

from collections import OrderedDict

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
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/specifications/mcps.csv"

        reader = CSVReader(filename=filename, cast=False)

        try:
            for row in reader.rows:
                mcp = cls.construct_from_jdict(json.loads(row))
                cls.__mcps[mcp.code] = mcp

        finally:
            reader.close()


    @classmethod
    def mcps(cls):
        for mcp in cls.__mcps.values():
            yield mcp


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
