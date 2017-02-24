"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# TODO: rename "sht" to "int" - requires clearance from OpenSensors.io

# --------------------------------------------------------------------------------------------------------------------

class GasesDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, afe_sample, sht_sample):
        """
        Constructor
        """
        val = []

        for key in afe_sample.sns:
            val.append((key, afe_sample.sns[key]))

        val.append(('pt1', afe_sample.pt1000))
        val.append(('sht', sht_sample))

        super().__init__(rec, *val)
