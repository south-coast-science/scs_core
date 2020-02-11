#!/usr/bin/env python3

"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log_reader import CSVLogReader
from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.datetime import LocalizedDatetime

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

log = conf.csv_log(topic_name, timeline_start=start_datetime)
print(log)
print("-")

queue = log.cursor_queue(rec_field)
print(queue)
print("-")

reader = CSVLogReader(queue)
print(reader)
print("-")

reader.start()

try:
    reader.join()
except KeyboardInterrupt:
    pass
