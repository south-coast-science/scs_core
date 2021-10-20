"""
Created on 2 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example request:
{"sample": {"tag": "test", "rec": "2020-11-11T16:16:34Z",
"val": {"NO2": {"weV": 0.31569, "aeV": 0.3095, "weC": 0.00395, "cnc": 11.6},
"CO": {"weV": 0.34176, "aeV": 0.25519, "weC": 0.09502, "cnc": 397.6},
"SO2": {"weV": 0.26657, "aeV": 0.26494, "weC": -0.00267, "cnc": 20.5},
"H2S": {"weV": 0.18319, "aeV": 0.26013, "weC": -0.04456, "cnc": 36.7},
"sht": {"hmd": 66.1, "tmp": 22.2}}},
"t-slope": 0.0, "rh-slope": 0.1,
"brd-tmp": 30.3}
"""

import json

from scs_core.comms.uds_client import UDSClient

from scs_core.data.json import JSONify
from scs_core.data.linear_regression import LinearRegression

from scs_core.model.gas.gas_inference_client import GasInferenceClient
from scs_core.model.gas.vB.gas_request import GasRequest

from scs_core.sync.schedule import ScheduleItem


# --------------------------------------------------------------------------------------------------------------------

class VBGasInferenceClient(GasInferenceClient):
    """
    classdocs
    """

    @classmethod
    def construct(cls, socket, inference_uds_path, gas_schedule_item: ScheduleItem):
        # UDS...
        uds_client = UDSClient(socket, inference_uds_path)

        # T / rH slope...
        slope_tally = GasRequest.slope_tally(gas_schedule_item.duration())

        t_regression = LinearRegression(tally=slope_tally)
        rh_regression = LinearRegression(tally=slope_tally)

        return cls(uds_client, t_regression, rh_regression)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client, t_regression, rh_regression):
        """
        Constructor
        """
        super().__init__(uds_client)

        self.__t_regression = t_regression                  # LinearRegression
        self.__rh_regression = rh_regression                # LinearRegression


    # ----------------------------------------------------------------------------------------------------------------

    def infer(self, gas_sample, board_temp):
        # T / rH slope...
        self.__t_regression.append(gas_sample.rec, gas_sample.sht_datum.temp)
        self.__rh_regression.append(gas_sample.rec, gas_sample.sht_datum.humid)

        m, _ = self.__t_regression.line()
        t_slope = 0.0 if m is None else m

        m, _ = self.__rh_regression.line()
        rh_slope = 0.0 if m is None else m

        # request...
        gas_request = GasRequest(gas_sample, t_slope, rh_slope, board_temp)

        # infer...
        self._uds_client.request(JSONify.dumps(gas_request))
        response = self._uds_client.wait_for_response()

        # report...
        return json.loads(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VBGasInferenceClient:{uds_client:%s, t_regression:%s, rh_regression:%s}" %  \
               (self._uds_client, self.__t_regression, self.__rh_regression)
