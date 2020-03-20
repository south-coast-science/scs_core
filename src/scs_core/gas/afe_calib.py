"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
4-Way AFE:
{"serial_number":"250011","type":"810-00000","pt1000_v20":2.0,"calibrated_on":null,"dispatched_on":null,
"sn1":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"287.0","we_total_zero_mv":"284.0", ...},
"sn2":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"287.0","we_total_zero_mv":"284.0", ...},
"sn3":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"280.0","we_total_zero_mv":"284.0", ...},
"sn4":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"313.0","we_total_zero_mv":"305.0", ...}}
"""

import json

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_core.gas.afe.pt1000_calib import Pt1000Calib

from scs_core.gas.sensor import Sensor
from scs_core.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class AFECalib(PersistentJSONable):
    """
    classdocs
    """

    ALPHASENSE_HOST =       "www.alphasense-technology.co.uk"
    ALPHASENSE_PATH =       "/api/v1/boards/"
    ALPHASENSE_HEADER =     {"Accept": "application/json"}

    TEST_LOAD = '''
                {"serial_number": "1", "type": "test-load", "calibrated_on": null, "dispatched_on": null, 
                "pt1000_v20": 1.0, 

                "sn1": {"serial_number": "01", "sensor_type": "SN1", "we_electronic_zero_mv": 1, 
                "we_sensor_zero_mv": 1, "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, 
                "ae_total_zero_mv": 1, "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", 
                "pcb_gain": 1.0, "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 

                "sn2": {"serial_number": "02", "sensor_type": "SN2", "we_electronic_zero_mv": 1, 
                "we_sensor_zero_mv": 1, "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, 
                "ae_total_zero_mv": 1, "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", 
                "pcb_gain": 1.0, "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 

                "sn3": {"serial_number": "03", "sensor_type": "SN3", "we_electronic_zero_mv": 1, 
                "we_sensor_zero_mv": 1, "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, 
                "ae_total_zero_mv": 1, "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", 
                "pcb_gain": 1.0, "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 

                "sn4": {"serial_number": "04", "sensor_type": "SN4", "we_electronic_zero_mv": 1, 
                "we_sensor_zero_mv": 1, "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, 
                "ae_total_zero_mv": 1, "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", 
                "pcb_gain": 1.0, "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}}    
                '''


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "afe_calib.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def download(cls, http_client, serial_number):
        http_client.connect(AFECalib.ALPHASENSE_HOST)

        try:
            path = AFECalib.ALPHASENSE_PATH + serial_number
            jdict = json.loads(http_client.get(path, None, AFECalib.ALPHASENSE_HEADER))

            return cls.construct_from_jdict(jdict)

        finally:
            http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        afe_type = jdict.get('type')

        calibrated_on = Datum.date(jdict.get('calibrated_on'))
        dispatched_on = Datum.date(jdict.get('dispatched_on'))

        pt1000_v20 = jdict.get('pt1000_v20')
        pt100_calib = None if pt1000_v20 is None else Pt1000Calib(calibrated_on, pt1000_v20)

        sensor_calibs = []

        for key in sorted(jdict.keys()):
            if key[:2] == "sn":
                if jdict[key] is None:
                    sensor_calibs.append(None)
                    continue

                sensor_calibs.append(SensorCalib.construct_from_jdict(jdict[key]))

        return AFECalib(serial_number, afe_type, calibrated_on, dispatched_on, pt100_calib, sensor_calibs)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, afe_type, calibrated_on, dispatched_on, pt100_calib, sensor_calibs):
        """
        Constructor
        """
        self.__serial_number = serial_number
        self.__afe_type = afe_type

        self.__calibrated_on = calibrated_on        # date
        self.__dispatched_on = dispatched_on        # date

        self.__pt100_calib = pt100_calib            # Pt1000Calib

        self.__sensor_calibs = sensor_calibs        # array of SensorCalib


    def __len__(self):
        return len(self.__sensor_calibs)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['type'] = self.afe_type

        jdict['calibrated_on'] = self.calibrated_on.isoformat() if self.calibrated_on else None
        jdict['dispatched_on'] = self.dispatched_on.isoformat() if self.dispatched_on else None

        jdict['pt1000_v20'] = self.pt1000_calib.v20 if self.pt1000_calib else None

        for i in range(len(self.__sensor_calibs)):
            jdict['sn' + str(i + 1)] = self.__sensor_calibs[i]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def sensors(self, afe_baseline):
        sensors = []
        for i in range(len(self)):
            calib = self.sensor_calib(i)
            sensor = None if calib is None else calib.sensor(afe_baseline.sensor_baseline(i))

            sensors.append(sensor)

        return sensors


    def gas_names(self):
        names = []
        for sensor_calib in self.__sensor_calibs:
            if sensor_calib is None:
                continue

            sensor = Sensor.find(sensor_calib.serial_number)
            name = sensor.gas_name

            names.append(name)

        return names


    def has_unique_gas_names(self):
        names = set()

        for sensor_calib in self.__sensor_calibs:
            if sensor_calib is None:
                continue

            sensor = Sensor.find(sensor_calib.serial_number)
            name = sensor.gas_name

            if name in names:
                return False

            names.add(name)

        return True


    def sensor_index(self, gas_name):
        for i in range(len(self.__sensor_calibs)):
            sensor_calib = self.__sensor_calibs[i]

            if sensor_calib is None:
                continue

            sensor = Sensor.find(sensor_calib.serial_number)

            if sensor.gas_name == gas_name:
                return i

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def afe_type(self):
        return self.__afe_type


    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @calibrated_on.setter
    def calibrated_on(self, calibrated_on):
        self.__calibrated_on = calibrated_on


    @property
    def dispatched_on(self):
        return self.__dispatched_on


    @property
    def pt1000_calib(self):
        return self.__pt100_calib


    def sensor_calib(self, i):
        return self.__sensor_calibs[i]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cls = self.__class__.__name__
        sensor_calibs = '[' + ', '.join(str(calib) for calib in self.__sensor_calibs) + ']'

        return cls + ":{serial_number:%s, afe_type:%s, calibrated_on:%s, " \
                     "dispatched_on:%s, pt100_calib:%s, sensor_calibs:%s}" %  \
                     (self.serial_number, self.afe_type, self.calibrated_on,
                      self.dispatched_on, self.pt1000_calib, sensor_calibs)
