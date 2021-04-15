#!/usr/bin/env python3

"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_core.psu.psu_version import PSUVersion


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"id": "South Coast Science PSU", "tag": "001.002.003", "c-date": "Aug  8 2017", "c-time": "08:35:25"}'
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

status = PSUVersion.construct_from_jdict(jdict)
print(status)
print("-")

jdict = status.as_json()
print(jdict)
print("-")

jstr = JSONify.dumps(jdict)
print(jstr)
print("-")
