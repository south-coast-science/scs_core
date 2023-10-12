#!/usr/bin/env python3

"""
Created on 1 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.monitor.alert.alert import AlertSpecification

from scs_core.data.json import JSONify
from scs_core.data.recurring_period import RecurringPeriod


# --------------------------------------------------------------------------------------------------------------------

aggregation_period = RecurringPeriod.construct(4, 'H', 'Europe/London')
test_interval = RecurringPeriod.construct(5, 'M', 'Europe/London')

alert = AlertSpecification(None, 'description', 'my/topic', 'my.field', None, 100, True, aggregation_period,
                           test_interval, True, 'bruno.beloff@southcoastscience.com',
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
