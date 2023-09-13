#!/usr/bin/env python3

"""
Created on 13 Sep 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client_traffic.client_traffic import ClientTrafficReport
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------


reports = [
    ClientTrafficReport('e1', 'c1', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e1', 'c2', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e1', 'c3', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e2', 'c1', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e2', 'c2', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e2', 'c3', '2023-09-01', 1, 10, 100),
    ClientTrafficReport('e1', 'c1', '2023-09-02', 1, 10, 100),
    ClientTrafficReport('e1', 'c2', '2023-09-02', 1, 10, 100),
    ClientTrafficReport('e1', 'c3', '2023-09-02', 1, 10, 100),
    ClientTrafficReport('e2', 'c1', '2023-09-02', 1, 10, 100),
    ClientTrafficReport('e2', 'c2', '2023-09-02', 1, 10, 100),
    ClientTrafficReport('e2', 'c3', '2023-09-02', 1, 10, 100),
]

print("reports...")
for report in reports:
    print(report)
print("-")

aggregations = ClientTrafficReport.client_aggregations('2023-09', reports)

print("aggregations...")
for report in aggregations:
    print(report)
print("-")

totals = ClientTrafficReport.organisation_totals('MyOrg', reports)

print("totals...")
for report in totals:
    print(report)
print("-")

aggregations = ClientTrafficReport.client_aggregations('2023-09', totals)

print("aggregations of totals...")
for report in aggregations:
    print(report)
print("-")

print(JSONify.dumps(aggregations, indent=4))
