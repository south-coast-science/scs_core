"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Parameter codes and associated standard units

NB: initialisation is performed at the foot of this class

example:
{"code": 88374, "description": "OC1 CSN_Rev Unadjusted PM2.5 LC", "unit-code": 105}

https://www.airnow.gov/
"""

import os

from collections import OrderedDict

from scs_core.aqcsv.specification.unit import Unit

from scs_core.csv.csv_archive import CSVArchive
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Parameter(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'parameters.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        code = jdict.get('code')
        description = jdict.get('description')
        unit_code = jdict.get('unit-code')

        return Parameter(code, description, unit_code)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, description, unit_code):
        """
        Constructor
        """
        self.__code = int(code)                             # int(5)
        self.__description = description                    # string
        self.__unit_code = int(unit_code)                   # int(3)


    def __eq__(self, other):
        try:
            return self.code == other.code and self.description == other.description and \
                   self.unit_code == other.unit_code

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['description'] = self.description
        jdict['unit-code'] = self.unit_code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.code


    def unit(self):
        return Unit.instance(self.unit_code)


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
        return "Parameter:{code:%05d, description:%s, unit_code:%03d}" % \
               (self.code, self.description, self.unit_code)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

Parameter.retrieve()
