"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-bgx-401",
 "rec": "2017-09-24T07:56:27.304+00:00",
 "val": {
  "tz": {"name": "Europe/London", "utc-offset": "+01:00"},
  "pos": {"lat": 50.8229247, "lng": -0.1229787, "qual": 2},
  "sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
    "scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
  "tmp": {"brd": 35.8, "hst": null},
  "up": {"period": "01-21:52:00.000", "users": 0, "load": {"av1": 0.0, "av5": 0.0, "av15": 0.0}},
  "psu": {"p-rst": false, "w-rst": false, "batt-flt": false, "host-3v3": 3.4, "pwr-in": 12.4, "prot-batt": 6.7}}}
"""

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, timezone, position, temperature, schedule, uptime, psu_status):
        """
        Constructor
        """
        val = []

        if timezone:
            val.append(('tz', timezone))

        if position:
            val.append(('pos', position))

        val.append(('sch', schedule))
        val.append(('tmp', temperature))
        val.append(('up', uptime))

        if psu_status:
            val.append(('psu', psu_status))

        super().__init__(tag, rec, *val)
