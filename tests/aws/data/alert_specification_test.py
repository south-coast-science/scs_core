#!/usr/bin/env python3

"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.data.alert import AlertSpecification, AlertStatus

from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

aggregation_period = RecurringPeriod.construct(5, 'M')
test_interval = Timedelta(minutes=5)

print("1...")

alert = AlertSpecification(None, 'my/topic', 'my.field', None, 100, True, aggregation_period, test_interval,
                           'bruno.beloff@southcoastscience.com', ["bbeloff@me.com", "hhopton@me.com"], False)
print(alert)

jstr = JSONify.dumps(alert)
print(jstr)

print("-")
print("2...")

alert = AlertSpecification.construct_from_jdict(json.loads(jstr))
alert.id = 123
print(alert)

print("-")
print("3...")

status = alert.status(50)
print(status)

status = alert.status(None)
print(status)

status = alert.status(9)
print(status)

status = alert.status(101.5)
print(status)

print("-")
print("4...")

jstr = JSONify.dumps(status)
print(jstr)

status = AlertStatus.construct_from_jdict(json.loads(jstr))
print(status)
