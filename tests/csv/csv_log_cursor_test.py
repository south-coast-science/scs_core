#!/usr/bin/env python3

"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue, CSVLogCursor

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

jobs = CSVLogCursorQueue()
print(jobs)
print("-")

print("include...")
cursor = CSVLogCursor('path/file1.csv', 0, False)
jobs.include(cursor)
print(jobs)
print("-")

print("include...")
cursor = CSVLogCursor('path/file2.csv', 0, True)
jobs.include(cursor)
print(jobs)
print("-")

jdict = jobs.as_json()
print(jdict)

print(JSONify.dumps(jdict))
print("-")

jobs = CSVLogCursorQueue.construct_from_jdict(jdict)
print(jobs)
print("=")


print("pop...")
job = jobs.pop()
print(job)
print(jobs)
print("-")

print("pop...")
job = jobs.pop()
print(job)
print(jobs)
print("-")

print("pop...")
job = jobs.pop()
print(job)
print(jobs)
print("-")
