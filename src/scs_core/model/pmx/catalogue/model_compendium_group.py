"""
Created on 7 June 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a group of machine learning model compendia, one for each PM size

By convention, the name of the group should be the same as the name of the ML model template.

document example:
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONCatalogueEntry
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.model.pmx.catalogue.model_compendium import ModelCompendium

from scs_core.sys.logging import Logging


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

        compendia = {pm: ModelCompendium.retrieve(compendium_name) for pm, compendium_name in compendia_jdict.items()}

        return cls(name, compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, compendia):
        """
        Constructor
        """
        self.__name = name
        self.__compendia = compendia                    # dict of pmx: ModelCompendium

        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def postprocess(self, response: PathDict):
        if not response.has_sub_path(sub_path='exg'):
            return None

        for pm, compendium in self.__compendia.items():
            model_output_path = '.'.join(('exg', 'val', pm, 'cnc'))
            model_output = float(response.node(model_output_path))

            corrected_exg = round(compendium.postprocess(model_output), 1)

            response.append(model_output_path, corrected_exg)
            self.__logger.debug("postprocess - %s model_output: %s" % (pm, model_output))

        return response.node('exg')


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, pm, compendium):
        self.__compendia[pm] = compendium


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def pms(self):
        return set(sorted(self.compendia.keys()))


    def compendium(self, gas):
        return self.__compendia[gas]


    @property
    def compendia(self):
        return self.__compendia


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['compendia'] = {pm: self.compendia[pm].name for pm in self.pms}

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        compendia = Str.collection(self.compendia)

        return "ModelCompendiumGroup:{name:%s, compendia:%s}" %  (self.name, compendia)
