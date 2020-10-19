#!/usr/bin/env python3

"""
Created on 14 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.disk_volume import DiskVolume, ReportedDiskVolume


# --------------------------------------------------------------------------------------------------------------------
# run...

volume = DiskVolume.construct_from_df_row('/dev/mmcblk1p2   3513504 2331488    983824  71% /')
print(volume)
print("percent_used: %s" % volume.percent_used())
print("-")

jstr = JSONify.dumps(volume)
print(jstr)

jdict = json.loads(jstr)
volume = ReportedDiskVolume.construct_from_jdict(jdict)
print(volume)

