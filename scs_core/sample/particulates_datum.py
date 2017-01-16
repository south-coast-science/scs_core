"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.sample.sample_datum import SampleDatum


# --------------------------------------------------------------------------------------------------------------------

class ParticulatesDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, sample):
        """
        Constructor
        """
        bins = OrderedDict([(i, sample.bins[i]) for i in range(len(sample.bins))])

        super().__init__(rec, ('pm1', sample.pm1), ('pm2p5', sample.pm2p5), ('pm10', sample.pm10), ('bins', bins),
                    ('mtf1', sample.bin_1_mtof), ('mtf3', sample.bin_3_mtof), ('mtf5', sample.bin_5_mtof), ('mtf7', sample.bin_7_mtof))
