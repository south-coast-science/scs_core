"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NB: initialisation is performed at the foot of this class

example document:
{"topic": "particulates", "species": "pm2p5", "source": "N3", "parameter-code": "88101", "unit-code": 105,
"qc-code": 0, "method-code": 195, "mpc-code": 1, "mpc-value": 5.0}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SourceMapping(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'source_mappings.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if jdict is None:
            return None

        topic = jdict.get('topic')
        species = jdict.get('species')
        source = jdict.get('source')

        parameter_code = jdict.get('parameter-code')
        unit_code = jdict.get('unit-code')
        qc_code = jdict.get('qc-code')
        method_code = jdict.get('method-code')
        mpc_code = jdict.get('mpc-code')

        mpc_value = jdict.get('mpc-value')

        return SourceMapping(topic, species, source,
                             parameter_code, unit_code, qc_code, method_code, mpc_code, mpc_value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, species, source,
                 parameter_code, unit_code, qc_code, method_code, mpc_code, mpc_value):
        """
        Constructor
        """
        self.__topic = topic                                        # string
        self.__species = species                                    # string
        self.__source = source                                      # string

        self.__parameter_code = parameter_code                      # int(5) or string
        self.__unit_code = Datum.int(unit_code)                     # int(3)
        self.__qc_code = Datum.int(qc_code)                         # int
        self.__method_code = Datum.int(method_code)                 # int(3)
        self.__mpc_code = Datum.int(mpc_code)                       # int

        self.__mpc_value = Datum.float(mpc_value, 5)                # numeric(10,5)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['species'] = self.species
        jdict['source'] = self.source

        jdict['parameter-code'] = self.parameter_code
        jdict['unit-code'] = self.unit_code
        jdict['qc-code'] = self.qc_code
        jdict['method-code'] = self.method_code
        jdict['mpc-code'] = self.mpc_code

        jdict['mpc-value'] = self.mpc_value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.topic, self.species, self.source


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def species(self):
        return self.__species


    @property
    def source(self):
        return self.__source


    @property
    def parameter_code(self):
        return self.__parameter_code


    @property
    def unit_code(self):
        return self.__unit_code


    @property
    def qc_code(self):
        return self.__qc_code


    @property
    def method_code(self):
        return self.__method_code


    @property
    def mpc_code(self):
        return self.__mpc_code


    @property
    def mpc_value(self):
        return self.__mpc_value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SourceMapping:{topic:%s, species:%s, source:%s, " \
               "parameter_code:%s, unit_code:%03d, qc_code:%d, method_code:%03d, mpc_code:%d, mpc_value:%0.5f}" % \
               (self.topic, self.species, self.source,
                self.parameter_code, self.unit_code, self.qc_code, self.method_code, self.mpc_code, self.mpc_value)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

SourceMapping.retrieve()
