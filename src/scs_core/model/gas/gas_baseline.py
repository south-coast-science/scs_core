"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}},
"NO2": {"calibrated-on": "2021-01-19T11:07:27Z", "offset": 1, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}}}
"""

from scs_core.data.str import Str
from scs_core.model.gas.baseline import Baseline


# --------------------------------------------------------------------------------------------------------------------

class GasBaseline(Baseline):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "gas_baseline.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_baselines):
        """
        Constructor
        """
        super().__init__(sensor_baselines)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GasBaseline:{sensor_baselines:%s}" % Str.collection(self.sensor_baselines)
