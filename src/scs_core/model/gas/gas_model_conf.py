"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for gases inference

example JSON:
{"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vE", "model-compendium-group": "oE.1"}
"""

from scs_core.gas.afe_calib import AFECalib

from scs_core.model.catalogue.model_compendium_group import ModelCompendiumGroup
from scs_core.model.gas.gas_baseline import GasBaseline
from scs_core.model.gas.gas_inference_client import GasInferenceClient
from scs_core.model.gas.vcal_baseline import VCalBaseline
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


    __INTERFACES = ('s1', 'vB', 'vB2', 'vE')

    @classmethod
    def interfaces(cls):
        return cls.__INTERFACES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_path, model_interface, model_compendium_group=None):
        """
        Constructor
        """
        super().__init__(uds_path, model_interface, model_compendium_group=model_compendium_group)


    # ----------------------------------------------------------------------------------------------------------------

    def client(self, host, socket, schedule_item: ScheduleItem) -> GasInferenceClient:
        # s1 (obsolete)...
        if self.model_interface == 's1':
            from scs_core.model.gas.s1.s1_gas_inference_client import S1GasInferenceClient

            afe_calib = AFECalib.load(host)

            return S1GasInferenceClient.construct(socket, self.abs_uds_path(host), schedule_item, afe_calib)

        # vB (document v1.0 and v2.0)...
        if self.model_interface == 'vB' or self.model_interface == 'vB2':
            from scs_core.model.gas.vB.vb_gas_inference_client import VBGasInferenceClient

            return VBGasInferenceClient.construct(socket, self.abs_uds_path(host), schedule_item)

        # vE (document v2.0)...
        if self.model_interface == 'vE':
            from scs_core.model.gas.vE.ve_gas_inference_client import VEGasInferenceClient

            vcal_baseline = VCalBaseline.load(host, skeleton=True)
            gas_baseline = GasBaseline.load(host, skeleton=True)
            model_compendium_group = ModelCompendiumGroup.retrieve(self.model_compendium_group)

            return VEGasInferenceClient.construct(socket, self.abs_uds_path(host), schedule_item, vcal_baseline,
                                                  gas_baseline, model_compendium_group)

        raise ValueError(self.model_interface)
