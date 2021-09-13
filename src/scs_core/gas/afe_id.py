"""
Created on 4 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"serial_number": "27-000001", "type": "810-0023-02", "calibrated_on": "2016-11-01",
"sn1": {"serial_number": "212060308", "sensor_type": "NO2A43F"},
"sn2": {"serial_number": "132950202", "sensor_type": "CO A4"},
"sn3": {"serial_number": "134060009", "sensor_type": "SO2A4"},
"sn4": {"serial_number": "133910023", "sensor_type": "H2SA4"}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class AFEId(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return AFECalib.persistence_location()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        afe_type = jdict.get('type')
        calibrated_on = Datum.date(jdict.get('calibrated_on'))

        sensor_ids = []

        for key in sorted(jdict.keys()):
            if key[:2] == "sn":
                if jdict[key] is None:
                    sensor_ids.append(None)
                    continue

                sensor_ids.append(SensorId.construct_from_jdict(jdict[key]))

        return cls(serial_number, afe_type, calibrated_on, sensor_ids)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, afe_type, calibrated_on, sensor_ids):
        """
        Constructor
        """
        super().__init__()

        self.__serial_number = serial_number            # string
        self.__afe_type = afe_type                      # string
        self.__calibrated_on = calibrated_on            # date

        self.__sensor_ids = sensor_ids                  # array of SensorId


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for i in range(len(self)):
                if self.sensor_id(i) != other.sensor_id(i):
                    return False

            return self.serial_number == other.serial_number and self.afe_type == other.afe_type and \
                self.calibrated_on == other.calibrated_on

        except (AttributeError, TypeError):
            return False


    def __len__(self):
        return len(self.__sensor_ids)


    # ----------------------------------------------------------------------------------------------------------------

    def sensor_index(self, gas_name):
        for i in range(len(self.__sensor_ids)):
            sensor_id = self.__sensor_ids[i]

            if sensor_id is None:
                continue

            sensor = Sensor.find(sensor_id.serial_number)

            if sensor is None:
                raise ValueError(sensor_id.serial_number)

            if sensor.gas_name == gas_name:
                return i

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['type'] = self.afe_type
        jdict['calibrated_on'] = self.calibrated_on.isoformat() if self.calibrated_on else None

        for i in range(len(self.__sensor_ids)):
            jdict['sn' + str(i + 1)] = self.__sensor_ids[i]

        return jdict


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


    def sensor_id(self, i):
        return self.__sensor_ids[i]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AFEId:{serial_number:%s, afe_type:%s, calibrated_on:%s, sensor_ids:%s}" %  \
                     (self.serial_number, self.afe_type, self.calibrated_on, Str.collection(self.__sensor_ids))


# --------------------------------------------------------------------------------------------------------------------

class SensorId(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        return cls(serial_number, sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type):
        """
        Constructor
        """
        self.__serial_number = serial_number                    # int
        self.__sensor_type = sensor_type                        # string


    def __eq__(self, other):
        try:
            return self.serial_number == other.serial_number and self.sensor_type == other.sensor_type

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def sensor_type(self):
        return self.__sensor_type


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorId:{serial_number:%s, sensor_type:%s}" %  (self.serial_number, self.sensor_type)
