"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for particulates inference

example JSON:
"""

from scs_core.model.model_conf import ModelConf


# --------------------------------------------------------------------------------------------------------------------

class PMxModelConf(ModelConf):
    """
    classdocs
    """

    __FILENAME = "pmx_model_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    __INTERFACES = ['s1']

    @classmethod
    def interfaces(cls):
        return cls.__INTERFACES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, resource_names):
        """
        Constructor
        """
        super().__init__(uds_path, model_interface, resource_names)


    # ----------------------------------------------------------------------------------------------------------------

    def client(self, host):
        if self.model_interface == 's1':
            from scs_core.model.particulates.s1.s1_pmx_inference_client import S1PMxInferenceClient
            return S1PMxInferenceClient.construct(self.abs_uds_path(host))

        raise ValueError(self.model_interface)
