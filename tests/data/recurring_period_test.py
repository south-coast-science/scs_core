#!/usr/bin/env python3

"""
Created on 7 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

print("json...")
period = RecurringPeriod.construct(1, 'D', 'Europe/London')
print(period)

jstr = JSONify.dumps(period)
print(jstr)
print("-")

print("day...")
period = RecurringPeriod.construct_from_jdict(json.loads(jstr))
print(period)
print(repr(period))

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))


end_datetime = period.end_datetime(now)
start_datetime = period.start_datetime(now)
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)
print("-")


print("hours...")
period = RecurringPeriod.construct(4, 'H', 'Europe/London')
print(period)
print(repr(period))

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))

end_datetime = period.end_datetime(now)
start_datetime = period.start_datetime(now)
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)
print("-")


print("minutes...")
period = RecurringPeriod.construct(5, 'M', 'Europe/London')
print(period)
print(repr(period))

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))

end_datetime = period.end_datetime(now)
start_datetime = period.start_datetime(now)
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)

