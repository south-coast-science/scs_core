#!/usr/bin/env python3

"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log import CSVLog
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

path = '/Users/bruno/Python/MacProject/scs_core/tests/csv'

log = CSVLog(path, 'gases', now)
print(log)
print("file_name: %s" % log.file_name())
print("-")

log.mkdir()
print("-")

for hours in range(5, 10):
    new_time = now.timedelta(hours=hours)
    print("offset: %s, new_time: %s" % (hours, new_time))
    print("is_in_timeline: %s" % log.in_timeline(new_time))

print("-")


path = 'data/2018-04'

log = CSVLog(path, 'gases', now)
print(log)
print("file_name: %s" % log.file_name())
print("-")

log.mkdir()
print("-")

