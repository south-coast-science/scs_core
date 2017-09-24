"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-bgb-113",
 "rec": "2017-09-24T07:54:28.687+00:00",
 "val": {
  "pm1": 14.0, "pm2p5": 16.4, "pm10": 22.2,
  "bins": {"0": 1482, "1": 230, "2": 72, "3": 14, "4": 7, "5": 6, "6": 7, "7": 2, "8": 5, "9": 3, "10": 0,
    "11": 0, "12": 0, "13": 0, "14": 0, "15": 0},
  "mtf1": 14, "mtf3": 18, "mtf5": 22, "mtf7": 31}}
"""

from collections import OrderedDict

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ParticulatesSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, sample):
        """
        Constructor
        """
        bins = OrderedDict([(i, sample.bins[i]) for i in range(len(sample.bins))])

        super().__init__(tag, rec, ('per', sample.period),
                         ('pm1', sample.pm1), ('pm2p5', sample.pm2p5), ('pm10', sample.pm10), ('bins', bins),
                         ('mtf1', sample.bin_1_mtof), ('mtf3', sample.bin_3_mtof), ('mtf5', sample.bin_5_mtof),
                         ('mtf7', sample.bin_7_mtof))
