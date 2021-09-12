"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract ML model group configuration
"""

import os

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ModelConf(ABC, PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def interfaces(cls):
        return []


    @classmethod
    def is_valid_interface(cls, model_interface):
        return model_interface in cls.interfaces()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        uds_path = jdict.get('uds-path')
        model_interface = jdict.get('model-interface')

        return cls(uds_path, model_interface)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface):
        """
        Constructor
        """
        super().__init__()

        self.__uds_path = uds_path                                  # string
        self.__model_interface = model_interface                    # string


    def __eq__(self, other):
        try:
            return self.uds_path == other.uds_path and self.model_interface == other.model_interface
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['uds-path'] = self.uds_path
        jdict['model-interface'] = self.model_interface

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{uds_path:%s, model_interface:%s}" %  \
               (self.uds_path, self.model_interface)
