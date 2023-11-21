"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a group of machine learning model compendia, one for each gas

By convention, the name of the group should be the same as the name of the ML model template.

document example:
{"name": "oE.1", "compendia": {"NO2": "NO2.vE.OPCube.21HA"}}
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONCatalogueEntry
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.model.gas.baseline import Baseline
from scs_core.model.catalogue.model_compendium import ModelCompendium

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

        compendia = {gas: ModelCompendium.retrieve(compendium_name) for gas, compendium_name in compendia_jdict.items()}

        return cls(name, compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, compendia):
        """
        Constructor
        """
        self.__name = name
        self.__compendia = compendia                    # dict of gas: ModelCompendium

        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.compendia)


    # ----------------------------------------------------------------------------------------------------------------

    def preprocess(self, datum: PathDict, offsets=None):
        if offsets is None:
            offsets = Baseline({})

        for gas, compendium in self.__compendia.items():
            datum = compendium.preprocess(datum, offset=offsets.sensor_offset(gas))

        return datum


    def postprocess(self, preprocessed: PathDict, response: PathDict):
        if not response.has_sub_path(sub_path='exg'):
            return None

        for gas, compendium in self.__compendia.items():
            try:
                vcal_excess_path = '.'.join(('sample', 'val', gas, 'vCalExtr'))
                vcal_excess = float(preprocessed.node(vcal_excess_path))

                model_output_path = '.'.join(('exg', 'val', gas, 'cnc'))
                model_output = float(response.node(model_output_path))

            except KeyError:
                continue

            for primary in compendium.primaries:
                corrected_exg = round(compendium.postprocess(primary, vcal_excess, model_output), 1)

                self.__logger.debug("postprocess - %s model_output: %s vcal_excess: %s corrected_exg: %s" %
                                    (gas, model_output, vcal_excess, corrected_exg))

                response.append(model_output_path, corrected_exg)

        return response.node('exg')


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
        return set(sorted(self.compendia.keys()))


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
