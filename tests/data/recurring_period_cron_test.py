#!/usr/bin/env python3

"""
Created on 14 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

print("day...")
period = RecurringPeriod.construct(1, 'D', 'Europe/London')
print(period)
print('    cron: %s' % period.cron(2))
print('aws_cron: %s' % period.aws_cron(2))
print("-")

print("day...")
period = RecurringPeriod.construct(1, 'D', 'Asia/Kolkata')
print(period)
print('    cron: %s' % period.cron(2))
print('aws_cron: %s' % period.aws_cron(2))
print("-")

print("hours...")
period = RecurringPeriod.construct(4, 'H', 'Asia/Kolkata')
print(period)
print('    cron: %s' % period.cron(2))
print('aws_cron: %s' % period.aws_cron(2))
print("-")


print("minutes...")
period = RecurringPeriod.construct(5, 'M', 'Asia/Kolkata')
print(period)
print('    cron: %s' % period.cron(2))
print('aws_cron: %s' % period.aws_cron(2))

