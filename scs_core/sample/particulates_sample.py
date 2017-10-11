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


{"tag": "scs-be2-3",
"rec": "2017-10-09T10:56:35.300+00:00",
"val": {
"per": NaN, "pm1": NaN, "pm2p5": NaN, "pm10": NaN,
"bins": {"0": -1, "1": -1, "2": -1, "3": -1, "4": -1, "5": -1, "6": -1, "7": -1, "8": -1, "9": -1,
 "10": -1, "11": -1, "12": -1, "13": -1, "14": -1, "15": -1}, "mtf1": 255, "mtf3": 255, "mtf5": 255, "mtf7": 255}}
"""

from collections import OrderedDict

from scs_core.sample.sample import Sample


# TODO: deal with NaN issue when OPC unavailable

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
