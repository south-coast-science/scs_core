"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.comms.uds_client import UDSClient

from scs_core.data.json import JSONify
from scs_core.data.linear_regression import LinearRegression
from scs_core.data.path_dict import PathDict

from scs_core.model.gas.gas_inference_client import GasInferenceClient
from scs_core.model.gas.vE.gas_request import GasRequest

from scs_core.sync.schedule import ScheduleItem

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class VEGasInferenceClient(GasInferenceClient):
    """
    classdocs
    """

    @classmethod
    def construct(cls, socket, inference_uds_path, schedule_item: ScheduleItem, vcal_baseline, gas_baseline,
                  model_compendium_group):
        # UDS...
        uds_client = UDSClient(socket, inference_uds_path)

        # T / rH slope...
        slope_tally = GasRequest.slope_tally(schedule_item.duration())

        t_regression = LinearRegression(tally=slope_tally)
        rh_regression = LinearRegression(tally=slope_tally)

        return cls(uds_client, t_regression, rh_regression, vcal_baseline, gas_baseline, model_compendium_group)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client, t_regression, rh_regression, vcal_baseline, gas_baseline, model_compendium_group):
        """
        Constructor
        """
        super().__init__(uds_client)

        self.__t_regression = t_regression                              # LinearRegression
        self.__rh_regression = rh_regression                            # LinearRegression

        self.__vcal_baseline = vcal_baseline                            # VCalBaseline
        self.__gas_baseline = gas_baseline                              # GasBaseline
        self.__model_compendium_group = model_compendium_group          # ModelCompendiumGroup

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def infer(self, gas_sample, board_temp):
        # T / rH slope...
        self.__t_regression.append(gas_sample.rec, gas_sample.sht_datum.temp)
        self.__rh_regression.append(gas_sample.rec, gas_sample.sht_datum.humid)

        m, _ = self.__t_regression.line()
        t_slope = 0.0 if m is None else m

        m, _ = self.__rh_regression.line()
        rh_slope = 0.0 if m is None else m

        # preprocess...
        request = PathDict(GasRequest(gas_sample, t_slope, rh_slope, board_temp).as_json())
        sample = request.node(sub_path='sample')

        preprocessed = self.__model_compendium_group.preprocess(request, self.__vcal_baseline)

        # infer...
        self._uds_client.request(JSONify.dumps(preprocessed))
        response = PathDict(json.loads(self._uds_client.wait_for_response()))

        if not response:
            self.__logger.error("request rejected: %s" % JSONify.dumps(gas_sample))
            return sample

        # postprocess...
        exg = PathDict(self.__model_compendium_group.postprocess(preprocessed, response))

        # gas baseline...
        for gas, offset in self.__gas_baseline.offsets().items():
            path = '.'.join(('val', gas, 'cnc'))
            node = exg.node(sub_path=path)

            baselined_cnc = round(float(node) + offset, 1)
            exg.append(path, round(baselined_cnc, 1))

        # report...
        report = PathDict(sample)                       # discard any changes made in preprocessing

        if exg is not None:
            report.append('ver', response.node(sub_path='ver'))
            report.append('exg', exg.node())

        return report.dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VEGasInferenceClient:{uds_client:%s, t_regression:%s, rh_regression:%s, vcal_baseline:%s, " \
               "gas_baseline:%s, model_compendium_group:%s}" %  \
               (self._uds_client, self.__t_regression, self.__rh_regression, self.__vcal_baseline,
                self.__gas_baseline, self.__model_compendium_group)
