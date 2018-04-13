#!/usr/bin/env python3

"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log_conf import CSVLogConf
from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

root_path = '/Volumes/SCS/data'

conf = CSVLogConf(root_path)
print(conf)
print("-")

conf.save(Host)

conf = CSVLogConf.load(Host)

print(conf)
print("-")

print(JSONify.dumps(conf.as_json()))
