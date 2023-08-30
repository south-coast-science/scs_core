#!/usr/bin/env python3

"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.client_traffic.client_traffic import ClientTrafficReport
from scs_core.aws.client_traffic.client_traffic_finder import ClientTrafficResponse

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

endpoint = 'aaa'
client = '111'
period = '2023-08-01'
queries = 10
invocations = 10
documents = 100

report1 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report1)

jstr = JSONify.dumps(report1)
print(jstr)

report2 = ClientTrafficReport.construct_from_jdict(json.loads(jstr))
print(report1)

print("equals: %s" % str(report1 == report2))
print("-")

endpoint = 'aaa'
client = '111'
period = '2023-08-02'
queries = 11
invocations = 11
documents = 110

report2 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report2)

endpoint = 'aaa'
client = '111'
period = '2023-08-03'
queries = 12
invocations = 12
documents = 120

report3 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report3)

endpoint = 'aaa'
client = '222'
period = '2023-08-03'
queries = 12
invocations = 12
documents = 120

report6 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report6)

endpoint = 'bbb'
client = '111'
period = '2023-08-02'
queries = 11
invocations = 11
documents = 110

report4 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report4)

endpoint = 'bbb'
client = '111'
period = '2023-08-03'
queries = 12
invocations = 12
documents = 120

report5 = ClientTrafficReport(endpoint, client, period, queries, invocations, documents)
print(report5)
print("-")

response = ClientTrafficResponse([report6, report5, report4, report3, report2, report1])

for item in sorted(response.items):
    print(item)
