"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-bgx-500", "rec": "2019-01-05T12:04:10Z", "val": {"tz": {"name": "Europe/London", "utc-offset": "+00:00"},
"gps": {"pos": [50.8230166, -0.1229759], "elv": 39.9, "qual": 1},
"sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"tmp": {"brd": 29.6}, "up": {"period": "00-00:31:00", "users": 1, "load": {"av1": 0.06, "av5": 0.07, "av15": 0.22}},
"psu": {"rst": "00", "standby": false, "chg": "0000", "batt-flt": false, "host-3v3": 3.4, "pwr-in": 15.8,
"prot-batt": 0.1}}}
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

        if timezone is not None:
            val.append(('tz', timezone))

        if position is not None:
            val.append(('gps', position))

        val.append(('sch', schedule))
        val.append(('tmp', temperature))
        val.append(('up', uptime))

        if psu_status is not None:
            val.append(('psu', psu_status))

        super().__init__(tag, None, rec, *val)
