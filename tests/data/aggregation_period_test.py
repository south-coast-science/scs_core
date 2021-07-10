#!/usr/bin/env python3

"""
Created on 7 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.aggregation_period import AggregationPeriod
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

print("json...")
period = AggregationPeriod.construct(1, 'D')
print(period)

jstr = JSONify.dumps(period)
print(jstr)
print("-")

print("day...")
period = AggregationPeriod.construct_from_jdict(json.loads(jstr))
print(period)

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))


end_datetime = period.end_datetime(now)
start_datetime = end_datetime - period.timedelta()
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)
print("-")


print("hours...")
period = AggregationPeriod.construct(4, 'H')
print(period)

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))

end_datetime = period.end_datetime(now)
start_datetime = end_datetime - period.timedelta()
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)
print("-")


print("minutes...")
period = AggregationPeriod.construct(5, 'M')
print(period)

print("is valid: %s" % period.is_valid())
print("checkpoint: %s" % period.checkpoint())
print("cron: %s" % period.cron(1))

end_datetime = period.end_datetime(now)
start_datetime = end_datetime - period.timedelta()
print("start: %s" % start_datetime)
print("  end: %s" % end_datetime)

