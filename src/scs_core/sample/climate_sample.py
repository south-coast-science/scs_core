"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-be2-2",
 "rec": "2017-09-24T07:52:40.489+00:00",
 "val": {"hmd": 56.2, "tmp": 22.2}}
"""

from scs_core.sample.sample import Sample


# TODO: add pressure

# --------------------------------------------------------------------------------------------------------------------

class ClimateSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, sample):
        """
        Constructor
        """
        super().__init__(tag, rec, ('hmd', sample.humid), ('tmp', sample.temp))
