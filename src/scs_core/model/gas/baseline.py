"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}},
"NO2": {"calibrated-on": "2021-01-19T11:07:27Z", "offset": 1, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}}}
"""

from abc import ABC
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_core.gas.sensor_baseline import SensorBaseline


# --------------------------------------------------------------------------------------------------------------------

class Baseline(PersistentJSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls({}) if skeleton else None

        sensor_baselines = {}

        for gas, baseline_jdict in jdict.items():
            sensor_baselines[gas] = SensorBaseline.construct_from_jdict(baseline_jdict)

        return cls(sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_baselines):
        """
        Constructor
        """
        super().__init__()

        self.__sensor_baselines = sensor_baselines          # dict of gas: SensorBaseline


    def __eq__(self, other):
        try:
            if list(self.gases) != list(other.gases):
                return False

            for gas in self.gases:
                if self.sensor_baseline(gas) != other.sensor_baseline(gas):
                    return False

            return True

        except (TypeError, AttributeError):
            return False


    def __len__(self):
        return len(self.__sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        for gas in sorted(self.__sensor_baselines.keys()):
            jdict[gas] = self.__sensor_baselines[gas]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gases(self):
        return set(sorted(self.__sensor_baselines.keys()))


    def offsets(self, gases=None):
        return {gas: self.sensor_offset(gas) for gas in (self.gases if gases is None else gases)}


    def sensor_offset(self, gas):
        baseline = self.sensor_baseline(gas)
        return 0 if baseline is None else baseline.offset


    def sensor_baseline(self, gas):
        try:
            return self.__sensor_baselines[gas]
        except KeyError:
            return None


    def set_sensor_baseline(self, gas, sensor_baseline):
        self.__sensor_baselines[gas] = sensor_baseline


    def remove_sensor_baseline(self, gas):
        try:
            del self.__sensor_baselines[gas]
            return True
        except KeyError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensor_baselines(self):
        return self.__sensor_baselines
