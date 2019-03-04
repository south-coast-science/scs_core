"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Qualifiers

example:
Qualifier:{code:Y, description:Elapsed sample time out of spec., type_code:QA, type_description:Quality Assurance}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archived import CSVArchived
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Qualifier(JSONable, CSVArchived):
    """
    classdocs
    """

    _persisted = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        dirname = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(dirname, 'archive', 'qualifiers.csv')


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
    def pk(self):
        return self.code


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
        return "Qualifier:{code:%s, description:%s, type_code:%s, type_description:%s}" % \
               (self.code, self.description, self.type_code, self.type_description)
