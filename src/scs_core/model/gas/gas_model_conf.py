"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for gases inference

example JSON:
{"uds-path": "pipes/lambda-model-gas-s1.uds", "model-interface": "vB2"}
"""

from scs_core.gas.afe_calib import AFECalib

from scs_core.model.gas.gas_inference_client import GasInferenceClient
from scs_core.model.model_conf import ModelConf

from scs_core.sync.schedule import ScheduleItem


# --------------------------------------------------------------------------------------------------------------------

class GasModelConf(ModelConf):
    """
    classdocs
    """

    __FILENAME = "gas_model_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    __INTERFACES = ['s1', 'vB', 'vB2', 'vE']

    @classmethod
    def interfaces(cls):
        return cls.__INTERFACES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, model_compendium):
        """
        Constructor
        """
        super().__init__(uds_path, model_interface, model_compendium)


    # ----------------------------------------------------------------------------------------------------------------

    def client(self, host, socket, gas_schedule_item: ScheduleItem, afe_calib: AFECalib) -> GasInferenceClient:
        # s1...
        if self.model_interface == 's1':
            from scs_core.model.gas.s1.s1_gas_inference_client import S1GasInferenceClient

            return S1GasInferenceClient.construct(socket, self.abs_uds_path(host), gas_schedule_item, afe_calib)

        # vB...
        if self.model_interface == 'vB' or self.model_interface == 'vB2':
            from scs_core.model.gas.vB.vb_gas_inference_client import VBGasInferenceClient

            return VBGasInferenceClient.construct(socket, self.abs_uds_path(host), gas_schedule_item)

        # vB...
        if self.model_interface == 'vE':
            from scs_core.model.gas.vE.ve_gas_inference_client import VEGasInferenceClient

            return VEGasInferenceClient.construct(socket, self.abs_uds_path(host), gas_schedule_item,
                                                  self.model_compendium)

        raise ValueError(self.model_interface)
