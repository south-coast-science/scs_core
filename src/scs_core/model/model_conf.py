"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract machine learning model group configuration
"""

import os

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.model.model_map import ModelMap
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ModelConf(ABC, PersistentJSONable):
    """
    classdocs
    """

    __TEMPLATE_NO_MODELS = 'm0'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def gg_ml_template(cls, gas_model_conf, pmx_model_conf):
        # no models...
        if not gas_model_conf and not pmx_model_conf:
            return cls.__TEMPLATE_NO_MODELS

        # PMx-only model...
        if not gas_model_conf and pmx_model_conf:
            return None if pmx_model_conf.model_map is None else pmx_model_conf.model_map.p_gg_ml_template

        # gas-only model...
        if gas_model_conf and not pmx_model_conf:
            raise ValueError('a gas model without a PMx model is not supported.')

        # gas and PMx models...
        gas_model_map = gas_model_conf.model_map
        pmx_model_map = pmx_model_conf.model_map

        if gas_model_map != pmx_model_map:
            raise ValueError("the gas model map '%s' does not match the PMx model map '%s'" %
                             (gas_model_map, pmx_model_map))

        return None if gas_model_conf.model_map is None else gas_model_conf.model_map.pg_gg_ml_template


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def interfaces(cls):
        return tuple()


    @classmethod
    def is_valid_interface(cls, model_interface):
        return model_interface in cls.interfaces()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None) if skeleton else None

        uds_path = jdict.get('uds-path')
        model_interface = jdict.get('model-interface')

        try:
            field = 'model-map' if 'model-map' in jdict else 'model-compendium-group'
            model_map = ModelMap.map(jdict.get(field))
        except KeyError:
            model_map = None

        return cls(uds_path, model_interface, model_map)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, model_map):
        """
        Constructor
        """
        super().__init__()

        self.__uds_path = uds_path                                      # string
        self.__model_interface = model_interface                        # string
        self.__model_map = model_map                                    # ModelMapping

        self._logger = Logging.getLogger()


    def __eq__(self, other):
        try:
            return self.uds_path == other.uds_path and self.model_interface == other.model_interface and \
                   self.model_map == other.model_map

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['uds-path'] = self.uds_path
        jdict['model-interface'] = self.model_interface
        jdict['model-map'] = self.model_map_name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def abs_uds_path(self, host):
        return os.path.join(host.scs_path(), self.uds_path)


    @property
    def uds_path(self):
        return self.__uds_path


    @property
    def model_interface(self):
        return self.__model_interface


    @property
    def model_map(self):
        return self.__model_map


    @property
    def model_map_name(self):
        return None if self.__model_map is None else self.__model_map.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        model_map_name = None if self.model_map is None else self.model_map.name

        return self.__class__.__name__ + ":{uds_path:%s, model_interface:%s, model_map:%s}" %  \
            (self.uds_path, self.model_interface, model_map_name)
