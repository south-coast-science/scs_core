#!/usr/bin/env python3

"""
Created on 22 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.join import Join
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

pk_is_iso8601 = True

left_set_path = 'praxis'
left_pk_path = 'recL'

left_data = [
    '{"recL": "2019-02-01T01:00:00Z", "val": {"NO2": {"weV": 0.297688, "cnc": 42.8, "aeV": 0.298432, "weC": 0.002844}, '
    '"sht": {"hmd": 79.0, "tmp": 3.0}}}',
    '{"recL": "2019-02-01T02:00:00Z", "val": {"NO2": {"weV": 0.297185, "cnc": 40.8, "aeV": 0.298467, "weC": 0.002271}, '
    '"sht": {"hmd": 78.4, "tmp": 3.1}}}',
    '{"recL": "2019-02-01T03:00:00Z", "val": {"NO2": {"weV": 0.298541, "cnc": 45.8, "aeV": 0.298426, "weC": 0.003701}, '
    '"sht": {"hmd": 79.6, "tmp": 3.0}}}',
    '{"recL": "2019-02-01T04:00:00Z", "val": {"NO2": {"weV": 0.299773, "cnc": 49.7, "aeV": 0.298492, "weC": 0.004841}, '
    '"sht": {"hmd": 79.8, "tmp": 3.0}}}',
    '{"recL": "2019-02-01T05:00:00Z", "val": {"NO2": {"weV": 0.300002, "cnc": 50.1, "aeV": 0.298557, "weC": 0.004955}, '
    '"sht": {"hmd": 79.5, "tmp": 3.2}}}'
]

right_set_path = 'ref'
right_pk_path = 'recR'

right_data = [
    '{"recR": "2019-02-01T02:00:00+00:00", "val": {"NO2": {"status": "P", "units": "ugm-3", "dns": 34.0}}}',
    '{"recR": "2019-02-01T03:00:00+00:00", "val": {"NO2": {"status": "P", "units": "ugm-3", "dns": 47.0}}}',
    '{"recR": "2019-02-01T04:00:00+00:00", "val": {"NO2": {"status": "P", "units": "ugm-3", "dns": 55.0}}}',
    '{"recR": "2019-02-01T05:00:00+00:00", "val": {"NO2": {"status": "P", "units": "ugm-3", "dns": 59.0}}}',
    '{"recR": "2019-02-01T06:00:00+00:00", "val": {"NO2": {"status": "P", "units": "ugm-3", "dns": 61.0}}}'
]


# --------------------------------------------------------------------------------------------------------------------

join = Join.construct(left_set_path, left_pk_path, right_set_path, right_pk_path, pk_is_iso8601)
print(join)
print("-")

print("left...")
for jstr in left_data:
    print(jstr)
print("-")

print("right...")
for jstr in right_data:
    print(jstr)
print("-")

print("import...")
for jstr in left_data:
    join.append_to_left(PathDict.construct_from_jstr(jstr))

for jstr in right_data:
    join.append_to_right(PathDict.construct_from_jstr(jstr))

print(join)
print("-")

print("inner...")
for row in join.inner():
    print(JSONify.dumps(row))
print("-")

print("left...")
for row in join.left():
    print(JSONify.dumps(row))
print("-")

print("right...")
for row in join.right():
    print(JSONify.dumps(row))
print("-")

print("full...")
for row in join.full():
    print(JSONify.dumps(row))
print("-")
