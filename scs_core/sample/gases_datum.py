"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# --------------------------------------------------------------------------------------------------------------------

class GasesDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, co2_datum, afe_datum, sht_datum):
        """
        Constructor
        """
        val = []

        if co2_datum:
            val.append(('CO2', co2_datum))

        if afe_datum:
            val.extend([(key, afe_datum.sns[key]) for key in afe_datum.sns])

            if afe_datum.pt1000:
                val.append(('pt1', afe_datum.pt1000))

            val.append(('sht', sht_datum))

        super().__init__(tag, rec, *val)
