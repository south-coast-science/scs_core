"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for particulates inference

example JSON:
{"uds-path": "pipes/lambda-model-pmx-s1.uds", "model-interface": "s1",
"resource-names": {"pm1": "/trained-models/pm1-s1-2020h1/xgboost-model",
"pm2p5": "/trained-models/pm2p5-s1-2020h1/xgboost-model",
"pm10": "/trained-models/pm10-s1-2020h1/xgboost-model"}}
"""

from scs_core.model.model_conf import ModelConf
from scs_core.model.pmx.pmx_inference_client import PMxInferenceClient


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

    def __init__(self, uds_path, model_interface):
        """
        Constructor
        """
        super().__init__(uds_path, model_interface)


    # ----------------------------------------------------------------------------------------------------------------

    def client(self, host) -> PMxInferenceClient:
        if self.model_interface == 's1':
            from scs_core.model.pmx.s1.s1_pmx_inference_client import S1PMxInferenceClient
            return S1PMxInferenceClient.construct(self.abs_uds_path(host))

        raise ValueError(self.model_interface)
