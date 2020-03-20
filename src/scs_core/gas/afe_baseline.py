"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sn1": {"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50, "env": {"hmd": 66.0, "tmp": 11.0, "pA": 99.0}},
"sn2": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0, "env": null},
"sn3": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0, "env": null},
"sn4": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0, "env": null}}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_core.gas.sensor_baseline import SensorBaseline


# TODO: rename as Interface Baseline (GSBaseline)

# --------------------------------------------------------------------------------------------------------------------

class AFEBaseline(PersistentJSONable):
    """
    classdocs
    """

    __SENSORS = 4       # TODO: better to find out how long the AFECalib is than to use a constant

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "afe_baseline.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return AFEBaseline([SensorBaseline(None, 0, None)] * cls.__SENSORS)

        sensor_baselines = []

        for i in range(len(jdict)):
            key = 'sn' + str(i + 1)

            base = SensorBaseline.construct_from_jdict(jdict[key]) if key in jdict else SensorBaseline(None, 0, None)
            sensor_baselines.append(base)

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
