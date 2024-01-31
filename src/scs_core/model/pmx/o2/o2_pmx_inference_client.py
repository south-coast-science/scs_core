"""
Created on 24 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example request:
{"sample": {"rec": "2024-01-24T14:32:35Z", "tag": "scs-be2-3", "ver": 2.0, "src": "N3",
"val": {"per": 4.1, "pm1": 3.4, "pm2p5": 5.8, "pm10": 6.1,
"bin": [276, 175, 80, 13, 11, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 27, "mtf3": 29, "mtf5": 40, "mtf7": 0, "sfr": 5.61,
"sht": {"hmd": 42.6, "tmp": 23.8}}},
"ext-sht": {"hmd": 46.6, "tmp": 24.9},
"slopes": {"ext-t": 0.1, "ext-rh": 0.2, "opc-t": 0.3, "opc-rh": 0.4}}
"""

import json

from scs_core.comms.uds_client import UDSClient

from scs_core.data.json import JSONify
from scs_core.data.linear_regression import LinearRegression

from scs_core.model.pmx.pmx_inference_client import PMxInferenceClient
from scs_core.model.pmx.o2.pmx_request import PMxRequest

from scs_core.sync.schedule import ScheduleItem

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class O2PMxInferenceClient(PMxInferenceClient):
    """
    classdocs
    """

    @classmethod
    def construct(cls, socket, inference_uds_path, schedule_item: ScheduleItem):
        # UDS...
        uds_client = UDSClient(socket, inference_uds_path)

        # T / rH slope...
        slope_tally = PMxRequest.slope_tally(schedule_item.duration())

        meteo_t_regression = LinearRegression(tally=slope_tally)
        meteo_rh_regression = LinearRegression(tally=slope_tally)

        opc_t_regression = LinearRegression(tally=slope_tally)
        opc_rh_regression = LinearRegression(tally=slope_tally)

        return cls(uds_client, meteo_t_regression, meteo_rh_regression, opc_t_regression, opc_rh_regression)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client, meteo_t_regression, meteo_rh_regression, opc_t_regression, opc_rh_regression):
        """
        Constructor
        """
        super().__init__(uds_client)

        self.__meteo_t_regression = meteo_t_regression                      # LinearRegression
        self.__meteo_rh_regression = meteo_rh_regression                    # LinearRegression

        self.__opc_t_regression = opc_t_regression                          # LinearRegression
        self.__opc_rh_regression = opc_rh_regression                        # LinearRegression

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def infer(self, opc_sample, ext_sht_datum):
        # self.__logger.error("opc_sample: %s" % opc_sample)
        # self.__logger.error("ext_sht_datum: %s" % ext_sht_datum)

        # Meteo T / rH slope...
        self.__meteo_t_regression.append(opc_sample.rec, ext_sht_datum.temp)
        meteo_t_slope = self.__meteo_t_regression.slope(default=0.0)

        self.__meteo_rh_regression.append(opc_sample.rec, ext_sht_datum.humid)
        meteo_rh_slope = self.__meteo_rh_regression.slope(default=0.0)

        # OPC T / rH slope...
        self.__opc_t_regression.append(opc_sample.rec, opc_sample.opc_datum.sht.temp)
        opc_t_slope = self.__opc_t_regression.slope(default=0.0)

        self.__opc_rh_regression.append(opc_sample.rec, opc_sample.opc_datum.sht.humid)
        opc_rh_slope = self.__opc_rh_regression.slope(default=0.0)

        # request...
        pmx_request = PMxRequest(opc_sample, ext_sht_datum, meteo_t_slope, meteo_rh_slope, opc_t_slope, opc_rh_slope)
        # self.__logger.info("pmx_request: %s" % pmx_request)

        self._uds_client.request(JSONify.dumps(pmx_request.as_json()))
        response = self._uds_client.wait_for_response()

        return json.loads(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "O2PMxInferenceClient:{uds_client:%s, meteo_t_regression:%s, meteo_rh_regression:%s, " \
               "opc_t_regression:%s, opc_rh_regression:%s}" %  \
            (self._uds_client, self.__meteo_t_regression, self.__meteo_rh_regression,
             self.__opc_t_regression, self.__opc_rh_regression)
