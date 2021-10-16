"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a group of machine learning model compendia, one for each gas

document example:
{"name": "OE.g1", "compendia": {"NO2": "NO2.vE.OPCube.21HA"}}
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONReport
from scs_core.data.str import Str

from scs_core.model.catalogue.model_compendium import ModelCompendium


# --------------------------------------------------------------------------------------------------------------------

class ModelCompendiumGroup(JSONReport):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def list(cls):
        return [cls.__filename_to_name(item) for item in sorted(os.listdir(cls.__catalogue_location()))
                if item.endswith('.json')]


    @classmethod
    def exists(cls, name):
        return name in cls.list()


    @classmethod
    def retrieve(cls, name):
        return cls.load(cls.catalogue_entry_location(name))


    @classmethod
    def catalogue_entry_location(cls, name):
        return os.path.join(cls.__catalogue_location(), cls.__name_to_filename(name))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __catalogue_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'groups')


    @classmethod
    def __name_to_filename(cls, name):
        return name.replace('.', '-') + '.json'


    @classmethod
    def __filename_to_name(cls, name):
        return name.replace('-', '.')[:-len('.json')]


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
        self.__name = name                              # string
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
    def filename(self):
        return self.catalogue_entry_location(self.name)


    def compendium(self, gas):
        return self.__compendia[gas]


    @property
    def compendia(self):
        return self.__compendia


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['compendia'] = {gas: self.compendia[gas].name for gas in sorted(self.compendia.keys())}

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        compendia = Str.collection(self.compendia)

        return "ModelCompendiumGroup:{name:%s, compendia:%s}" %  (self.name, compendia)
