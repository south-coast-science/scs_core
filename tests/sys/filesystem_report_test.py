#!/usr/bin/env python3

"""
Created on 25 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_logger_conf import CSVLoggerConf
from scs_core.data.json import JSONify
from scs_core.sys.filesystem_report import FilesystemReport

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

DATA_STORE = "/srv/removable_data_store"

data_log_1 = FilesystemReport.construct(DATA_STORE)
print("data_log_1: %s" % data_log_1)
print(JSONify.dumps(data_log_1))
print("-")

conf = CSVLoggerConf.load(Host)
print("conf: %s" % conf)

data_log_2 = conf.filesystem_report()
print("data_log_2: %s" % data_log_2)

print("equals: %s" % str(data_log_1 == data_log_2))
