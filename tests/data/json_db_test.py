#!/usr/bin/env python3

"""
Created on 1 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.data.alert import Alert

from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

aggregation_period = Timedelta(days=1)
test_interval = Timedelta(minutes=5)

alert = Alert(None, 'my/topic', 'my.field', None, 100, True, aggregation_period, test_interval,
              'bruno.beloff@southcoastscience.com', ["bbeloff@me.com", "hhopton@me.com"], False)
print(alert)
print("-")

print("as_dynamo_db...")
jdict = JSONify.as_dynamo_json(alert)
print(jdict)
print("-")

print("jstr...")
jstr = JSONify.dumps(jdict)
print(jstr)
print("-")

alert = Alert.construct_from_jdict(json.loads(jstr))
print(alert)
