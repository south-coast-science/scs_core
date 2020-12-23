"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for gases inference

example JSON:
{"uds-path": "pipes/lambda-model-gas-s1.uds", "model-interface": "s1",
"model-filenames": {"NO2": "/trained-models/no2-s1-2020q13/xgboost-model"}}
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

    def client(self, host, gas_schedule_item, afe_calib):
        if self.model_interface == 's1':
            from scs_core.model.gas.s1.gas_inference_client import GasInferenceClient
            return GasInferenceClient.construct(self.abs_uds_path(host), gas_schedule_item, afe_calib)

        if self.model_interface == 's2':
            from scs_core.model.gas.s2.gas_inference_client import GasInferenceClient
            return GasInferenceClient.construct(self.abs_uds_path(host), gas_schedule_item)

        raise ValueError(self.model_interface)
