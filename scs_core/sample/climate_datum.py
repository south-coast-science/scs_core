"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# --------------------------------------------------------------------------------------------------------------------

class ClimateDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, sample):
        """
        Constructor
        """
        super().__init__(rec, ('hmd', sample.humid), ('tmp', sample.temp))
