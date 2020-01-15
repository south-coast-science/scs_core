#!/usr/bin/env python3

"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log import CSVLog
from scs_core.csv.csv_log_reader import CSVLogReader
from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = CSVLoggerConf.load(Host)
print(conf)

log = CSVLog(conf.root_path, 'gases')
print(log)

reader = CSVLogReader(Host, log)
print(reader)

print("-")

start = LocalizedDatetime.construct_from_iso8601('2019-01-24T13:37:00Z')
print(start)

print("-")

reader.read(start.datetime)

