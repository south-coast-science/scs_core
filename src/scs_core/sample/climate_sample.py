"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-ap1-6", "rec": "2019-01-22T13:55:54Z", "val": {"hmd": 49.3, "tmp": 21.5, "bar": {"pA": 99.8}}}
"""

from collections import OrderedDict

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ClimateSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, sht_sample, barometer_sample):
        """
        Constructor
        """
        jdict = OrderedDict()

        jdict['hmd'] = sht_sample.humid
        jdict['tmp'] = sht_sample.temp
        jdict['bar'] = barometer_sample

        super().__init__(tag, None, rec, jdict)
