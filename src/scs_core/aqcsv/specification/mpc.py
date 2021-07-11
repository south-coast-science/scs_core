"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Measurement performance characteristics

NB: initialisation is performed at the foot of this class

example:
{"code": 2, "abbreviation": "XC", "definition": "Critical Value",
"description": "Threshold above which a measurement result is unlikely to result from a true value of zero"}

https://www.airnow.gov/
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MPC(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'mpcs.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        code = jdict.get('code')
        abbreviation = jdict.get('abbreviation')
        definition = jdict.get('definition')
        description = jdict.get('description')

        return MPC(code, abbreviation, definition, description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, abbreviation, definition, description):
        """
        Constructor
        """
        self.__code = int(code)                                 # int
        self.__abbreviation = abbreviation                      # string
        self.__definition = definition                          # string
        self.__description = description                        # string


    def __eq__(self, other):
        try:
            return self.code == other.code and self.abbreviation == other.abbreviation and \
                   self.definition == other.definition and self.description == other.description

        except AttributeError:
            return False


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
    def pk(self):
        return self.code


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
        return "MPC:{code:%d, abbreviation:%s, definition:%s, description:%s}" % \
               (self.code, self.abbreviation, self.definition, self.description)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

MPC.retrieve()
