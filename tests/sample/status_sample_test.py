#!/usr/bin/env python3

"""
Created on 17 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sample.status_sample import StatusSample


# --------------------------------------------------------------------------------------------------------------------
# run...

jstr = '{"tag": "scs-bgx-600", "rec": "2020-11-17T12:07:34Z", ' \
       '"val": {"tz": {"name": "Europe/London", "utc-offset": "+00:00"}, ' \
       '"gps": {"pos": [50.82312142, -0.12319416], "elv": 44.0, "qual": 0}, ' \
       '"sch": {"scs-climate": {"interval": 10.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1}, ' \
       '"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}, ' \
       '"tmp": {"brd": 30.1}, ' \
       '"up": {"period": "26-02:37:00", "users": 0, "load": {"av1": 1.28, "av5": 1.56, "av15": 1.61}}, ' \
       '"psu": {"src": "Ov1", "standby": "False", "in": "True", "pwr-in": 12.3, "rst": 0, "chg": 0, ' \
       '"batt-flt": "False", "host-3v3": 3.3, "prot-batt": 0.0}}}'

print(jstr)
print("-")

jdict = json.loads(jstr)

sample = StatusSample.construct_from_jdict(jdict)
print(sample)
print("-")

print(JSONify.dumps(sample))

