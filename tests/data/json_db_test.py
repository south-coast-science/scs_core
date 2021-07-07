#!/usr/bin/env python3

"""
Created on 1 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.data.alert import AlertSpecification

from scs_core.data.aggregation_period import AggregationPeriod
from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

aggregation_period = AggregationPeriod.construct(4, 'H')
test_interval = Timedelta(minutes=5)

alert = AlertSpecification(None, 'my/topic', 'my.field', None, 100, True, aggregation_period, test_interval,
                           'bruno.beloff@southcoastscience.com', ["bbeloff@me.com", "hhopton@me.com"], False)
print(alert)
print("-")

print("as_dynamo_json...")
jdict = alert.as_dynamo_json()
print(jdict)
print("-")

print("jstr...")
jstr = JSONify.dumps(jdict)
print(jstr)
print("-")

alert = AlertSpecification.construct_from_jdict(json.loads(jstr))
print(alert)