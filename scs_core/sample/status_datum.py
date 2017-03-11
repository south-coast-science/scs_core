"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# --------------------------------------------------------------------------------------------------------------------

class StatusDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, location, temperature, exception):
        """
        Constructor
        """
        super().__init__(tag, rec, ('loc', location), ('tmp', temperature), ('exc', exception))
