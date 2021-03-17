"""
Created on 2 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example request:
{"particulates":
    {"tag": "scs-be2-3", "src": "N3", "rec": "2020-08-16T07:52:24Z",
    "val": {"per": 4.9, "pm1": 17.8, "pm2p5": 19.4, "pm10": 19.5,
    "bin": [703, 32, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "mtf1": 79, "mtf3": 80, "mtf5": 0, "mtf7": 0, "sfr": 0.52,
    "sht": {"hmd": 45.8, "tmp": 30.1}},
    "exg": {"ISLin/N3/vPLHR": {"pm1": 41.0, "pm2p5": 21.0, "pm10": 15.3}}},
"climate":
    {"hmd": 60.5, "tmp": 25.9}}
"""

import json

from scs_core.comms.uds_client import UDSClient

from scs_core.data.json import JSONify

from scs_core.model.pmx.pmx_inference_client import PMxInferenceClient
from scs_core.model.pmx.s1.pmx_request import PMxRequest


# --------------------------------------------------------------------------------------------------------------------

class S1PMxInferenceClient(PMxInferenceClient):
    """
    classdocs
    """

    @classmethod
    def construct(cls, socket, inference_uds_path):
        # UDS...
        uds_client = UDSClient(socket, inference_uds_path)

        return cls(uds_client)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client):
        """
        Constructor
        """
        super().__init__(uds_client)


    # ----------------------------------------------------------------------------------------------------------------

    def infer(self, opc_sample, ext_sht_sample):
        pmx_request = PMxRequest(opc_sample, ext_sht_sample)

        self._uds_client.request(JSONify.dumps(pmx_request.as_json()))
        response = self._uds_client.wait_for_response()

        return json.loads(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "S1PMxInferenceClient:{uds_client:%s}" %  self._uds_client
