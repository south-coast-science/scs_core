"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an ML model group configuration for particulates inference

example JSON:
{"uds-path": "pipes/lambda-model-pmx-s1.uds", "model-interface": "s1"}
"""

from scs_core.model.model_conf import ModelConf
from scs_core.model.pmx.pmx_inference_client import PMxInferenceClient

from scs_core.sync.schedule import ScheduleItem


# --------------------------------------------------------------------------------------------------------------------

class PMxModelConf(ModelConf):
    """
    classdocs
    """

    __FILENAME = "pmx_model_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    __INTERFACES = ('s1', 's2')

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

    def client(self, host, socket, schedule_item: ScheduleItem) -> PMxInferenceClient:
        # oE.2...
        if self.model_compendium_group and self.model_compendium_group.endswith('oE.2'):
            from scs_core.model.pmx.o2.o2_pmx_inference_client import O2PMxInferenceClient

            return O2PMxInferenceClient.construct(socket, self.abs_uds_path(host), schedule_item)

        # others...
        if self.model_interface == 's1' or self.model_interface == 's2':
            from scs_core.model.pmx.s1.s1_pmx_inference_client import S1PMxInferenceClient

            return S1PMxInferenceClient.construct(socket, self.abs_uds_path(host))

        raise ValueError(self.model_interface)
