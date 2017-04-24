"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sn1": {"calibrated_on": "2017-03-01", "offset": 111}, "sn2": {"calibrated_on": "2017-03-01", "offset": 222},
"sn3": {"calibrated_on": "2017-03-01", "offset": 333}, "sn4": {"calibrated_on": "2017-03-01", "offset": 444}}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.gas.sensor_baseline import SensorBaseline


# TODO: similar to AFECalib, this class should be backed by the cloud helper system

# --------------------------------------------------------------------------------------------------------------------

class AFEBaseline(PersistentJSONable):
    """
    classdocs
    """

    __SENSORS = 4       # TODO: better to find out how long the AFECalib is than to use a constant?

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "afe_baseline.json"

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
            return AFEBaseline([SensorBaseline(None, 0)] * cls.__SENSORS)

        sensor_baselines = []

        for i in range(len(jdict)):
            key = 'sn' + str(i + 1)

            baseline = SensorBaseline.construct_from_jdict(jdict[key]) if key in jdict else SensorBaseline(None, 0)
            sensor_baselines.append(baseline)

        return AFEBaseline(sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_baselines):
        """
        Constructor
        """
        self.__sensor_baselines = sensor_baselines        # array of SensorBaseline


    def __len__(self):
        return len(self.__sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


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
        sensor_baselines = '[' + ', '.join(str(baseline) for baseline in self.__sensor_baselines) + ']'

        return "AFEBaseline:{sensor_baselines:%s}" % sensor_baselines
