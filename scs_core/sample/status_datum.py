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

    def __init__(self, tag, rec, location, temperature, uptime):
        """
        Constructor
        """
        val = []

        if location:
            val.append(('loc', location))

        val.append(('tmp', temperature))
        val.append(('up', uptime))

        super().__init__(tag, rec, *val)
