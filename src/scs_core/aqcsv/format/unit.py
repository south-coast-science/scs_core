"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"code": "083", "description": "Cubic meters/minute STP"}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_persisted import CSVPersisted
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Unit(JSONable, CSVPersisted):
    """
    classdocs
    """

    _persisted = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(dirname, 'specifications', 'units.csv')


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
    def pk(self):
        return self.code


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
