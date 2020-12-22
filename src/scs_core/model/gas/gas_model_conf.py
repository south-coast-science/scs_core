"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for gases inference

example JSON:
{"uds_path": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false,
"inf": "/home/scs/SCS/pipes/lambda-uds_path-pmx-s1.uds", "exg": []}
"""

from scs_core.model.model_conf import ModelConf


# --------------------------------------------------------------------------------------------------------------------

class GasModelConf(ModelConf):
    """
    classdocs
    """

    __FILENAME = "gas_model_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    __INTERFACES = ['s1', 's2']

    @classmethod
    def interfaces(cls):
        return cls.__INTERFACES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, model_filenames):
        """
        Constructor
        """
        super().__init__(uds_path, model_interface, model_filenames)


    # ----------------------------------------------------------------------------------------------------------------

    def client(self):
        return self.model_interface


    def greengrass_interface(self):
        return self.model_interface


    def greengrass_request(self):
        return self.model_interface
