#!/usr/bin/env python3

"""
Created on 4 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

iso_str = '2023-01-04T12:47:22.123456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime)
print("rounded 0: %s" % rounded)
print("-")

iso_str = '2023-01-04T12:47:22.623456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime)
print("rounded 0: %s" % rounded)
print("=")


iso_str = '2023-01-04T12:47:30.123456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 1)
print("rounded 1: %s" % rounded)
print("-")

iso_str = '2023-01-04T12:47:30.623456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 1)
print("rounded 1: %s" % rounded)
print("=")


iso_str = '2023-01-04T12:30:30.123456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 2)
print("rounded 2: %s" % rounded)
print("-")

iso_str = '2023-01-04T12:30:30.623456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 2)
print("rounded 2: %s" % rounded)
print("=")


iso_str = '2023-01-04T12:30:30.123456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 3)
print("rounded 3: %s" % rounded)
print("-")

iso_str = '2023-01-04T12:30:30.623456Z'
print(iso_str)

datetime = LocalizedDatetime.construct_from_iso8601(iso_str)
print(datetime)

rounded = round(datetime, 3)
print("rounded 3: %s" % rounded)
print("=")

