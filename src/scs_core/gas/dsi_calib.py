"""
Created on 11 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"serial_number": "10-000056", "type": "810-0021-00", "calibrated_on": "YYYY-MM-DD", "dispatched_on": null,
"pt1000_v20": 1.0, "sn1": {"serial_number": "NNNNNNNNN", "sensor_type": "NOGA4", "we_electronic_zero_mv": 300,
"we_sensor_zero_mv": 6, "we_total_zero_mv": 300, "ae_electronic_zero_mv": 300, "ae_sensor_zero_mv": 1,
"ae_total_zero_mv": 300, "we_sensitivity_na_ppb": S.SSSSSSS, "we_cross_sensitivity_no2_na_ppb": -0.3,
"pcb_gain": -0.7, "we_sensitivity_mv_ppb": 0.2, "we_cross_sensitivity_no2_mv_ppb": 0.2}}
"""

import json

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class DSICalib(AFECalib):
    """
    classdocs
    """

    DSI_WRAPPER = '''
                {"serial_number": "00-000000", "type": "ISI", "calibrated_on": "YYYY-MM-DD", 
                "dispatched_on": null, "pt1000_v20": 1.0, 
                "sn1": {"serial_number": "NNNNNNNNN", "sensor_type": "A4", "we_electronic_zero_mv": 300, 
                "we_sensor_zero_mv": 0, "we_total_zero_mv": 300, "ae_electronic_zero_mv": 300, 
                "ae_sensor_zero_mv": 0, "ae_total_zero_mv": 300, "we_sensitivity_na_ppb": "S.SSSSSSS", 
                "we_cross_sensitivity_no2_na_ppb": -0.3, "pcb_gain": -0.7, "we_sensitivity_mv_ppb": 0.2, 
                "we_cross_sensitivity_no2_mv_ppb": "n/a"}}
                '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def download(cls, http_client, serial_number):
        http_client.connect(AFECalib.ALPHASENSE_HOST)

        try:
            path = SensorCalib.ALPHASENSE_PATH + serial_number
            jstr = http_client.get(path, None, SensorCalib.ALPHASENSE_HEADER)

            return cls.construct_from_jdict(json.loads(jstr))

        finally:
            http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        sensor_calib = SensorCalib.construct_from_jdict(jdict)
        sensor_calib.set_defaults()
        sensor_calib.set_sens_mv_from_sens_na()

        return cls('DSI', sensor_calib)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, afe_type, sensor_calib):
        """
        Constructor
        """
        super().__init__(None, afe_type, None, None, None, [sensor_calib])
