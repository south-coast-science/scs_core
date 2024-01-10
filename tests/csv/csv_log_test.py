#!/usr/bin/env python3

"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_data_log import CSVDataLog, CSVDataLogFile

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

device_tag = 'scs-sys-001'
topic_subject = 'gases'

now = LocalizedDatetime.now().utc()

path = '/home/pi/SCS/scs_core/tests/csv'

log = CSVDataLog(path, topic_subject, device_tag)
log.timeline_start = now

print(log)
print("file_name: %s" % CSVDataLogFile.name(now.datetime, topic_subject, device_tag))
print("file_path: %s" % log.file_path())
print("-")

log.mkdir()
print("-")

for hours in range(5, 18):
    new_time = now.timedelta(hours=hours)
    print("offset: %s, new_time: %s" % (hours, new_time))
    print("is_in_timeline: %s" % log.in_timeline(new_time))

print("-")

path = 'data'

log = CSVDataLog(path, topic_subject, device_tag)
log.timeline_start = now

print(log)
print("file_name: %s" % CSVDataLogFile.name(now.datetime, topic_subject, device_tag))
print("file_path: %s" % log.file_path())
print("-")

log.mkdir()
print("-")
