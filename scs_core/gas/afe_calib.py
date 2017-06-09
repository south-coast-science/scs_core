"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"serial_number":"250011","type":"810-00000","pt1000_v20":2.0,"calibrated_on":null,"dispatched_on":null,
"sn1":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"287.0","we_total_zero_mv":"284.0","ae_sensor_zero_mv":"7.0","sensor_ae_zero_na":"-5.1","sensor_we_zero_na":"-6.6","we_sensor_zero_mv":"9.0","ae_electronic_zero_mv":"280.0","we_electronic_zero_mv":"275.0","we_sensitivity_mv_ppb":"219.0","sensor_we_sensitivity_na_ppm":"-300.0","sensor_we_cross_sensitivity_na_ppm":"n/a","we_cross_sensitivity_ox_no2_mv_ppb":"n/a"},
"sn2":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"287.0","we_total_zero_mv":"284.0","ae_sensor_zero_mv":"2.0","sensor_ae_zero_na":"1.6","sensor_we_zero_na":"3.2","we_sensor_zero_mv":"4.0","ae_electronic_zero_mv":"285.0","we_electronic_zero_mv":"280.0","we_sensitivity_mv_ppb":"200.0","sensor_we_sensitivity_na_ppm":"250.0","sensor_we_cross_sensitivity_na_ppm":"n/a","we_cross_sensitivity_ox_no2_mv_ppb":"n/a"},
"sn3":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"280.0","we_total_zero_mv":"284.0","ae_sensor_zero_mv":"10.0","sensor_ae_zero_na":"-7.3","sensor_we_zero_na":"-4.4","we_sensor_zero_mv":"6.0","ae_electronic_zero_mv":"270.0","we_electronic_zero_mv":"278.0","we_sensitivity_mv_ppb":"292.0","sensor_we_sensitivity_na_ppm":"-400.0","sensor_we_cross_sensitivity_na_ppm":"-350.0","we_cross_sensitivity_ox_no2_mv_ppb":"256.0"},
"sn4":{"serial_number":"123456789","sensor_type":"IRMA1","ae_total_zero_mv":"313.0","we_total_zero_mv":"305.0","ae_sensor_zero_mv":"9.0","sensor_ae_zero_na":"7.2","sensor_we_zero_na":"4.8","we_sensor_zero_mv":"6.0","ae_electronic_zero_mv":"304.0","we_electronic_zero_mv":"299.0","we_sensitivity_mv_ppb":"400.0","sensor_we_sensitivity_na_ppm":"500.0","sensor_we_cross_sensitivity_na_ppm":"n/a","we_cross_sensitivity_ox_no2_mv_ppb":"n/a"}}
"""

from collections import OrderedDict

from scs_core.gas.sensor import Sensor

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable
from scs_core.gas.a4_calib import A4Calib
from scs_core.gas.pid_calib import PIDCalib
from scs_core.gas.pt1000_calib import Pt1000Calib


# --------------------------------------------------------------------------------------------------------------------

class AFECalib(PersistentJSONable):
    """
    classdocs
    """

    HOST =          "www.alphasense-technology.co.uk"
    PATH =          "/api/v1/boards/"
    HEADER =        {"Accept": "application/json"}

    TEST_JSON = '''
                {"serial_number": "1", "type": "test-load", "calibrated_on": null, "dispatched_on": null, 
                "pt1000_v20": 1.0, 
            
                "sn1": {"serial_number": "01", "sensor_type": "SN1", "we_electronic_zero_mv": 1, "we_sensor_zero_mv": 1, 
                "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, "ae_total_zero_mv": 1, 
                "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 1.0, 
                "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 
            
                "sn2": {"serial_number": "02", "sensor_type": "SN2", "we_electronic_zero_mv": 1, "we_sensor_zero_mv": 1, 
                "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, "ae_total_zero_mv": 1, 
                "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 1.0, 
                "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 
            
                "sn3": {"serial_number": "03", "sensor_type": "SN3", "we_electronic_zero_mv": 1, "we_sensor_zero_mv": 1, 
                "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, "ae_total_zero_mv": 1, 
                "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 1.0, 
                "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, 
            
                "sn4": {"serial_number": "04", "sensor_type": "SN4", "we_electronic_zero_mv": 1, "we_sensor_zero_mv": 1, 
                "we_total_zero_mv": 1, "ae_electronic_zero_mv": 1, "ae_sensor_zero_mv": 1, "ae_total_zero_mv": 1, 
                "we_sensitivity_na_ppb": 1.0, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 1.0, 
                "we_sensitivity_mv_ppb": 1.0, "we_cross_sensitivity_no2_mv_ppb": "n/a"}}    
                '''

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "afe_calib.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


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
        pt100_calib = Pt1000Calib(calibrated_on, pt1000_v20) if pt1000_v20 is not None else None

        sensor_calibs = []

        for key in sorted(jdict.keys()):
            if key[:2] == "sn":
                if jdict[key] is None:
                    sensor_calibs.append(None)
                    continue

                sensor_type = jdict[key]['sensor_type']

                if sensor_type[-2:] == 'A4' or sensor_type[:2] == 'SN':
                    sensor_calibs.append(A4Calib.construct_from_jdict(jdict[key]))

                elif sensor_type[:3] == 'PID':
                    sensor_calibs.append(PIDCalib.construct_from_jdict(jdict[key]))

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

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


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
        return [Sensor.find(sensor_calib.serial_number).gas_name for sensor_calib in self.__sensor_calibs]


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
        sensor_calibs = '[' + ', '.join(str(calib) for calib in self.__sensor_calibs) + ']'

        return "AFECalib:{serial_number:%s, afe_type:%s, calibrated_on:%s, dispatched_on:%s, pt100_calib:%s, " \
               "sensor_calibs:%s}" % \
               (self.serial_number, self.afe_type, self.calibrated_on, self.dispatched_on, self.pt1000_calib,
                sensor_calibs)
