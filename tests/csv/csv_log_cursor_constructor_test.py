#!/usr/bin/env python3

"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log import CSVLog
from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue
from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

start_iso = '2020-01-20T09:50:00Z'
topic_name = 'climate'
rec_field = 'rec'

start = LocalizedDatetime.construct_from_iso8601(start_iso)
start_datetime = start.datetime

print("start_datetime: %s" % start_datetime)
print("-")

conf = CSVLoggerConf.load(Host)
print(conf)

log = CSVLog(conf.root_path, topic_name, None, start_datetime)
print(log)

print("-")

queue = CSVLogCursorQueue.construct_for_log(log, rec_field)
print(queue)
