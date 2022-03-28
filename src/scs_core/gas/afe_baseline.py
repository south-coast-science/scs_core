"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sn1": {"calibrated-on": "2022-03-21T11:46:43Z", "offset": -1,
"env": {"rec": "2022-03-16T07:45:00Z", "hmd": 51.6, "tmp": 21.8}},
"sn2": {"calibrated-on": "2022-03-21T11:46:48Z", "offset": 44,
"env": {"rec": "2022-03-16T06:15:00Z", "hmd": 48.1, "tmp": 22.0}},
"sn3": {"calibrated-on": null, "offset": 0, "env": null},
"sn4": {"calibrated-on": "2022-03-21T11:46:37Z", "offset": 174,
"env": {"rec": "2022-03-16T06:30:00Z", "hmd": 48.2, "tmp": 21.9}}}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.data.str import Str

from scs_core.gas.sensor_baseline import SensorBaseline


# --------------------------------------------------------------------------------------------------------------------

class AFEBaseline(PersistentJSONable):
    """
    classdocs
    """

    __SENSORS = 4       # TODO: better to find out how long the AFECalib is than to use a constant

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "afe_baseline.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls.null_datum() if skeleton else None

        sensor_baselines = []

        for i in range(len(jdict)):
            key = 'sn' + str(i + 1)

            base = SensorBaseline.construct_from_jdict(jdict[key]) if key in jdict else SensorBaseline.null_datum()
            sensor_baselines.append(base)

        return cls(sensor_baselines)


    @classmethod
    def null_datum(cls):
        return cls([SensorBaseline.null_datum()] * cls.__SENSORS)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_baselines):
        """
        Constructor
        """
        super().__init__()

        self.__sensor_baselines = sensor_baselines        # array of SensorBaseline


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for i in range(len(self)):
                if self.sensor_baseline(i) != other.sensor_baseline(i):
                    return False

                return True

        except (TypeError, AttributeError):
            return False


    def __len__(self):
        return len(self.__sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        for i in range(len(self.__sensor_baselines)):
            jdict['sn' + str(i + 1)] = self.__sensor_baselines[i]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def sensor_baseline(self, i):
        return self.__sensor_baselines[i]


    def set_sensor_baseline(self, i, sensor_baseline):
        self.__sensor_baselines[i] = sensor_baseline


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AFEBaseline:{sensor_baselines:%s}" % Str.collection(self.__sensor_baselines)
