#!/usr/bin/env python3

"""
Created on 13 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.ps_datum import PsDatum


# --------------------------------------------------------------------------------------------------------------------
# run...

report = "  154 26605   502 ??        0.0   0.0   0:00.37 01-00:43:12 /usr/bin/ssh-agent -l"
# report = "154 39364   502 ??        6.3  31.5  22:58.40    02:26:25 /Applications/PyCharm.app/Contents/MacOS/pycharm"
print(report)
print("-")

status = PsDatum.construct_from_report(report)
print(status)
print("-")

jstr = JSONify.dumps(status)
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

status = PsDatum.construct_from_jdict(jdict)
print(status)
print("-")
