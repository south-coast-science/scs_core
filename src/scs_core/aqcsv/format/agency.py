"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Agency codes

example:
{"code": "LBL", "name": "Lawrence Berkeley National Laboratory"}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_persisted import CSVPersisted
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Agency(JSONable, CSVPersisted):
    """
    classdocs
    """

    _persisted = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(dirname, 'specifications', 'agencies.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        name = jdict.get('name')

        return Agency(code, name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, name):
        """
        Constructor
        """
        self.__code = code                                  # string
        self.__name = name                                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['name'] = self.name

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
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Agency:{code:%s, name:%s}" % (self.code, self.name)
