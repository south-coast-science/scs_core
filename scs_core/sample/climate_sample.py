"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample import Sample


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
