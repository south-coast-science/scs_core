"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: quality control (QC) codes

example:
{"code": "1", "definition": "Adjusted"}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_persisted import CSVPersisted
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class QC(JSONable, CSVPersisted):
    """
    classdocs
    """

    _persisted = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(dirname, 'specifications', 'qcs.csv')


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
    def pk(self):
        return self.code


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def definition(self):
        return self.__definition


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "QC:{code:%s, definition:%s}" % (self.code, self.definition)
