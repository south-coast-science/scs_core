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

from scs_core.gas.afe_calib import AFECalib


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
    def construct_for_sensor(cls, calibrated_on, sensor_calib):
        return AFECalib(None, 'ISI', calibrated_on, None, None, [sensor_calib])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, afe_type, calibrated_on, dispatched_on, pt100_calib, sensor_calibs):
        """
        Constructor
        """
        super().__init__(serial_number, afe_type, calibrated_on, dispatched_on, pt100_calib, sensor_calibs)
