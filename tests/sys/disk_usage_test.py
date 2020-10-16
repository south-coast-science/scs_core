#!/usr/bin/env python3

"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import os

from scs_core.data.json import JSONify
from scs_core.sys.disk_usage import DiskUsage, ReportedDiskUsage


# --------------------------------------------------------------------------------------------------------------------
# run...

statvfs = os.statvfs('/')

usage = DiskUsage.construct_from_statvfs('/', statvfs)
print(usage)
print("percent_used: %s" % usage.percent_used())
print("-")

jstr = JSONify.dumps(usage)
print(jstr)

jdict = json.loads(jstr)
usage = ReportedDiskUsage.construct_from_jdict(jdict)
print(usage)

