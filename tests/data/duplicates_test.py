#!/usr/bin/env python3

"""
Created on 2 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.duplicates import Duplicates
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

data = [
    '{"rec": "2019-02-01T01:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 34.0}}}',
    '{"rec": "2019-02-01T02:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 34.0}}}',
    '{"rec": "2019-02-01T03:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 47.0}}}',
    '{"rec": "2019-02-01T04:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 55.0}}}',
    '{"rec": "2019-02-01T05:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 59.0}}}',
    '{"rec": "2019-02-01T06:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 61.0}}}',
    '{"rec": "2019-02-01T04:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 55.0}}}',
    '{"rec": "2019-02-01T05:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 59.0}}}',
    '{"rec": "2019-02-01T05:00:00+00:00", "val": {"NO2": {"status": "P", "dns": 59.0}}}'
]


# --------------------------------------------------------------------------------------------------------------------

dupes = Duplicates()
print("dupes: %s" % dupes)
print("-")

index = 0

# test...
for jstr in data:
    index += 1

    datum = PathDict.construct_from_jstr(jstr)
    key = datum.node('rec')

    is_duplicate = dupes.test(index, key, datum)

    print("key: %s is_duplicate: %s" % (key, is_duplicate))

print("dupes: %s" % dupes)
print("-")

# report...
print("keys: %s" % dupes.keys)
print("matched_key_count: %s" % dupes.matched_key_count)
print("max_index: %s" % dupes.max_index)
print("-")

print("matched_keys: %s" % [key for key in dupes.matched_keys()])
print("-")

for count in dupes.match_counts():
    print(JSONify.dumps(count))
print("-")

for match in dupes.matches():
    print(JSONify.dumps(match))
