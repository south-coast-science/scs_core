"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-be2-2",
 "rec": "2017-09-24T07:51:21.510+00:00",
 "val": {
  "NO2": {"weV": 0.312317, "aeV": 0.31038, "weC": -0.001, "cnc": 14.8},
  "CO": {"weV": 0.325005, "aeV": 0.254254, "weC": 0.077239, "cnc": 323.2},
  "SO2": {"weV": 0.277942, "aeV": 0.267754, "weC": 0.004136, "cnc": 27.6},
  "H2S": {"weV": 0.221816, "aeV": 0.269817, "weC": -0.006301, "cnc": 29.6},
  "pt1": {"v": 0.321411, "tmp": 21.9},
  "sht": {"hmd": 73.0, "tmp": 21.4}}}
"""

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class GasesSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, ndir_datum, afe_datum, sht_datum):
        """
        Constructor
        """
        val = []

        if ndir_datum:
            val.append(('CO2', ndir_datum))

        if afe_datum:
            val.extend([(key, afe_datum.sns[key]) for key in afe_datum.sns])

            if afe_datum.pt1000:
                val.append(('pt1', afe_datum.pt1000))

            if sht_datum:
                val.append(('sht', sht_datum))

        super().__init__(tag, rec, *val)
