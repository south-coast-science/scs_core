"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"NO2": {"calibrated-on": "2022-03-21T11:46:45Z", "offset": -31,
"env": {"rec": "2022-03-16T05:10:00Z", "hmd": 48.3, "tmp": 22.4}}}
"""

from scs_core.data.str import Str
from scs_core.model.gas.baseline import Baseline


# --------------------------------------------------------------------------------------------------------------------

class VCalBaseline(Baseline):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "vcal_baseline.json"

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
        return "VCalBaseline:{sensor_baselines:%s}" % Str.collection(self.sensor_baselines)
