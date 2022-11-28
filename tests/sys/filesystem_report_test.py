#!/usr/bin/env python3

"""
Created on 25 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.csv.csv_logger_conf import CSVLoggerConf
from scs_core.data.json import JSONify
from scs_core.sys.filesystem import FilesystemReport

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = CSVLoggerConf.load(Host)
print("conf: %s" % conf)
print("-")

data_log_1 = conf.filesystem_report()
print("data_log_1: %s" % data_log_1)
jstr = JSONify.dumps(data_log_1)
print(jstr)
print("-")

data_log_2 = FilesystemReport.construct_from_jdict(json.loads(jstr))
print("data_log_2: %s" % data_log_2)
print("-")

print("equals: %s" % str(data_log_1 == data_log_2))
