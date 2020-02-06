"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-ap1-6", "rec": "2019-03-09T12:05:10Z", "val":
{"airnow": {"site": "850MM123456789", "pocs": {"88102": 2, "88103": 3}},
"tz": {"name": "Europe/London", "utc-offset": "+00:00"},
"sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"tmp": {"brd": 30.2, "hst": 47.8},
"up": {"period": "00-18:30:00", "users": 2, "load": {"av1": 0.0, "av5": 0.0, "av15": 0.0}}}}
"""

from collections import OrderedDict

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, airnow, rec, timezone, position, temperature, schedule, uptime, psu_report):
        """
        Constructor
        """
        jdict = OrderedDict()

        if airnow is not None:
            jdict['airnow'] = airnow

        if timezone is not None:
            jdict['tz'] = timezone

        if position is not None:
            jdict['gps'] = position

        jdict['sch'] = schedule
        jdict['tmp'] = temperature
        jdict['up'] = uptime

        if psu_report is not None:
            jdict['psu'] = psu_report

        super().__init__(tag, None, rec, jdict)
