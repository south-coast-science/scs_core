"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a group of machine learning model compendia, one for each gas

document example:
{"name": "OE.g1", "compendia": {"NO2": "NO2.vE.OPCube.21HA"}}
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONCatalogueEntry
from scs_core.data.str import Str

from scs_core.model.catalogue.model_compendium import ModelCompendium


# --------------------------------------------------------------------------------------------------------------------

class ModelCompendiumGroup(JSONCatalogueEntry):
    """
    classdocs
    """

    __CATALOGUE_NAME = 'groups'

    @classmethod
    def catalogue_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), cls.__CATALOGUE_NAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, {}) if skeleton else None

        name = jdict.get('name')
        compendia_jdict = jdict.get('compendia')

        compendia = {gas: ModelCompendium.retrieve(compendium_name) for gas, compendium_name in compendia_jdict.items()}

        return cls(name, compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, compendia):
        """
        Constructor
        """
        self.__name = name
        self.__compendia = compendia                    # dict of gas: ModelCompendium


    def __len__(self):
        return len(self.compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, gas, compendium):
        self.__compendia[gas] = compendium


    def exclude(self, gas):
        if gas in self.compendia:
            del self.__compendia[gas]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def gases(self):
        return sorted(self.compendia.keys())


    def compendium(self, gas):
        return self.__compendia[gas]


    @property
    def compendia(self):
        return self.__compendia


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['compendia'] = {gas: self.compendia[gas].name for gas in self.gases}

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        compendia = Str.collection(self.compendia)

        return "ModelCompendiumGroup:{name:%s, compendia:%s}" %  (self.name, compendia)
