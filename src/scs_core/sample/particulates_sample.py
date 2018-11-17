"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example documents:

OPC-N2:
{"tag": "scs-be2-2", "src": "N2", "rec": "2018-11-11T09:05:10.424+00:00",
"val": {"per": 10.0, "pm1": 8.1, "pm2p5": 12.1, "pm10": 12.9,
"bins": [142, 63, 48, 28, 10, 13, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 42, "mtf3": 44, "mtf5": 46, "mtf7": 59}}

OPC-N3:
{"tag": "scs-be2-3", "src": "N3", "rec": "2018-11-17T12:06:45.605+00:00",
"val": {"per": 4.5, "pm1": 12.0, "pm2p5": 19.6, "pm10": 79.0,
"bins": [708, 27, 8, 3, 3, 3, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 81, "mtf3": 98, "mtf5": 97, "mtf7": 118,
"sht": {"hmd": 37.3, "tmp": 24.7}}}
"""

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
        val = [('per', sample.period), ('pm1', sample.pm1), ('pm2p5', sample.pm2p5), ('pm10', sample.pm10),
               ('bins', sample.bins), ('mtf1', sample.bin_1_mtof), ('mtf3', sample.bin_3_mtof),
               ('mtf5', sample.bin_5_mtof), ('mtf7', sample.bin_7_mtof)]

        if sample.sht is not None:
            val.append(('sht', sample.sht))

        super().__init__(tag, sample.source, rec, *val)
