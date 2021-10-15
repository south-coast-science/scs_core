"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example request:
{"sample": {"rec": "2021-10-15T09:14:38Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE",
"val": {"NO2": {"weV": 0.29, "aeV": 0.29557, "weC": 0.0005, "cnc": 17.9, "vCal": 12.799},
"Ox": {"weV": 0.39951, "aeV": 0.39988, "weC": 0.00196, "cnc": 54.6, "vCal": 1.795, "xCal": -0.392451},
"CO": {"weV": 0.37994, "aeV": 0.28975, "weC": 0.09457, "cnc": 409.5, "vCal": 380.414},
"sht": {"hmd": 58.6, "tmp": 22.3}}}, "t-slope": -0.1, "rh-slope": 0.2, "brd-tmp": 32.5}
"""

import json

from scs_core.comms.uds_client import UDSClient

from scs_core.data.json import JSONify
from scs_core.data.linear_regression import LinearRegression

from scs_core.model.gas.gas_inference_client import GasInferenceClient
from scs_core.model.gas.vE.gas_request import GasRequest

from scs_core.sync.schedule import ScheduleItem


# --------------------------------------------------------------------------------------------------------------------

class VEGasInferenceClient(GasInferenceClient):
    """
    classdocs
    """

    @classmethod
    def construct(cls, socket, inference_uds_path, gas_schedule_item: ScheduleItem, model_compendium_group):
        # UDS...
        uds_client = UDSClient(socket, inference_uds_path)

        # T / rH slope...
        slope_tally = GasRequest.slope_tally(gas_schedule_item.duration())

        t_regression = LinearRegression(tally=slope_tally)
        rh_regression = LinearRegression(tally=slope_tally)

        return cls(uds_client, t_regression, rh_regression, model_compendium_group)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client, t_regression, rh_regression, model_compendium_group):
        """
        Constructor
        """
        super().__init__(uds_client)

        self.__t_regression = t_regression                              # LinearRegression
        self.__rh_regression = rh_regression                            # LinearRegression
        self.__model_compendium_group = model_compendium_group          # ModelCompendiumGroup


    # ----------------------------------------------------------------------------------------------------------------

    def infer(self, gas_sample, board_temp):
        # T / rH slope...
        self.__t_regression.append(gas_sample.rec, gas_sample.sht_datum.temp)
        self.__rh_regression.append(gas_sample.rec, gas_sample.sht_datum.humid)

        m, _ = self.__t_regression.line()
        t_slope = 0.0 if m is None else m

        m, _ = self.__rh_regression.line()
        rh_slope = 0.0 if m is None else m

        # TODO: preprocess

        # request...
        gas_request = GasRequest(gas_sample, t_slope, rh_slope, board_temp)
        self._uds_client.request(JSONify.dumps(gas_request))

        response = self._uds_client.wait_for_response()

        # TODO: postprocess

        return json.loads(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VEGasInferenceClient:{uds_client:%s, t_regression:%s, rh_regression:%s, model_compendium_group:%s}" %  \
               (self._uds_client, self.__t_regression, self.__rh_regression, self.__model_compendium_group)
