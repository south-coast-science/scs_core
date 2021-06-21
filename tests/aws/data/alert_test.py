#!/usr/bin/env python3

"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.data.alert import Alert, AlertStatus

from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

aggregation_period = Timedelta(days=1)
test_interval = Timedelta(minutes=5)

alert = Alert('my/topic', 'my.field', None, None, 100, True,
              aggregation_period, test_interval, 'bruno.beloff@southcoastscience.com',
              ["bbeloff@me.com", "hhopton@me.com"], False)
alert.id = 123
print(alert)

jstr = JSONify.dumps(alert)
print(jstr)

alert = Alert.construct_from_jdict(json.loads(jstr))
print(alert)
print("-")

status = alert.status(50)
print(status)

status = alert.status(None)
print(status)

status = alert.status(9)
print(status)

status = alert.status(101.5)
print(status)
print("-")

jstr = JSONify.dumps(status)
print(jstr)

status = AlertStatus.construct_from_jdict(json.loads(jstr))
print(status)
print("-")

qsp = alert.params()
print(qsp)
print("-")

alert = Alert.construct_from_qsp(qsp)
print(alert)

