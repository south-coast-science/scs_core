#!/usr/bin/env python3

"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.monitor.alert.alert import AlertSpecification, AlertStatus

from scs_core.data.diurnal_period import DiurnalPeriod
from scs_core.data.json import JSONify
from scs_core.data.recurring_period import RecurringPeriod

from scs_core.email.email import EmailRecipient

# --------------------------------------------------------------------------------------------------------------------

aggregation_period = RecurringPeriod.construct(5, 'M', 'Europe/London')
test_interval = RecurringPeriod.construct(1, 'M', 'Europe/London')

to = EmailRecipient("bruno.beloff@southcoastscience.com", False)
r1 = EmailRecipient("bbeloff@me.com", False)
r2 = EmailRecipient("hhopton@me.com", False)
bcc_dict = {r1.email_address: r1, r2.email_address: r2}

print("1...")

alert = AlertSpecification(None, 'my description', 'my/topic', 'my.field', None, 100, True, aggregation_period,
                           test_interval, True, 'bruno.beloff@southcoastscience.com',
                           to, bcc_dict, False)
print(alert)
print("-")

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

print("5...")
start_time_str = '9:00'
end_time_str = '17:00'
timezone_str = 'Europe/London'

aggregation_period = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)

alert = AlertSpecification(None, 'my description', 'my/topic', 'my.field', None, 100, True, aggregation_period,
                           test_interval, False, 'bruno.beloff@southcoastscience.com',
                           to, bcc_dict, False)
print(alert)
print("-")

jstr = JSONify.dumps(alert)
print(jstr)
print("-")

alert = AlertSpecification.construct_from_jdict(json.loads(jstr))
print(alert)
print("-")
