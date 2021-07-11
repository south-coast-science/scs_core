"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Qualifiers

NB: initialisation is performed at the foot of this class

example:
{"code": "BL", "description": "QA audit", "type-code": "ND", "type-description": "Null Data"}

https://www.airnow.gov/
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Qualifier(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'qualifiers.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
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


    def __eq__(self, other):
        try:
            return self.code == other.code and self.description == other.description and \
                   self.type_code == other.type_code and self.type_description == other.type_description

        except AttributeError:
            return False


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


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

Qualifier.retrieve()
