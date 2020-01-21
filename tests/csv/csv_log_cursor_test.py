#!/usr/bin/env python3

"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.csv.csv_log_cursor import CSVLogCursorList
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

jobs = CSVLogCursorList(OrderedDict())
print(jobs)
print("-")

print("include...")
jobs.include('path/file1.csv', 22)
print(jobs)
print("-")

print("include...")
jobs.include('path/file2.csv')
print(jobs)
print("-")

jdict = jobs.as_json()
print(jdict)

print(JSONify.dumps(jdict))
print("-")

jobs = CSVLogCursorList.construct_from_jdict(jdict)
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
