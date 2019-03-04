"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AirNow quality control (QC) codes

example:
{"code": "1", "definition": "Adjusted"}
"""

import json
import os

from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class QC(JSONable):
    """
    classdocs
    """

    __qcs = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = dirname + "/specifications/qcs.csv"

        reader = CSVReader(filename, cast=False)

        try:
            for row in reader.rows:
                qc = cls.construct_from_jdict(json.loads(row))
                cls.__qcs[qc.code] = qc

        finally:
            reader.close()


    @classmethod
    def qcs(cls):
        for qc in cls.__qcs.values():
            yield qc


    @classmethod
    def find_by_code(cls, code):
        if code not in cls.__qcs:
            return None

        return cls.__qcs[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        definition = jdict.get('definition')

        return QC(code, definition)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, definition):
        """
        Constructor
        """
        self.__code = code                                  # string
        self.__definition = definition                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['definition'] = self.definition

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def definition(self):
        return self.__definition


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "QC:{code:%s, definition:%s}" %  (self.code, self.definition)
