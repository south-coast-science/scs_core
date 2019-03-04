"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Parameter codes and associated standard units

example:
{"code": "88502", "description": "Acceptable PM2.5 AQI Mass", "unit_code": "105"}
"""

import os

from collections import OrderedDict

from scs_core.aqcsv.specification.unit import Unit

from scs_core.csv.csv_archived import CSVArchived
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Parameter(JSONable, CSVArchived):
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
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        description = jdict.get('description')
        unit_code = str(jdict.get('unit-code'))

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
        jdict['unit-code'] = self.unit_code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.code


    @property
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
        return "Parameter:{code:%s, description:%s, unit_code:%s}" % (self.code, self.description, self.unit_code)
