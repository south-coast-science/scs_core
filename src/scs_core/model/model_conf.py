"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract ML model group configuration

example JSON:
{"uds_path": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false,
"inf": "/home/scs/SCS/pipes/lambda-uds_path-pmx-s1.uds", "exg": []}
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
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        uds_path = jdict.get('uds-path')
        model_interface = jdict.get('model-interface')
        model_filenames = jdict.get('model-filenames')

        return cls(uds_path, model_interface, model_filenames)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, model_filenames):
        """
        Constructor
        """
        self.__uds_path = uds_path                                  # string
        self.__model_interface = model_interface                    # string
        self.__model_filenames = model_filenames                    # dict of string: string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['uds-path'] = self.uds_path
        jdict['model-interface'] = self.model_interface
        jdict['model-filenames'] = self.model_filenames

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def set_filename(self, species, filename):
        self.__model_filenames[species] = filename


    def delete_filename(self, species):
        try:
            del self.__model_filenames[species]
        except KeyError:
            pass


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
    def model_filenames(self):
        return self.__model_filenames


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{uds_path:%s, model_interface:%s, model_filenames:%s}" %  \
               (self.uds_path, self.model_interface, self.model_filenames)
