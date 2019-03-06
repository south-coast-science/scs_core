#!/usr/bin/env python3

"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import sys

from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.sync.schedule import Schedule
from scs_core.sync.schedule import ScheduleItem


# --------------------------------------------------------------------------------------------------------------------
# run...

item1 = ScheduleItem('one', 1.11, 1)
print(item1)

item2 = ScheduleItem('two', 2.25, 2)
print(item2)

item3 = ScheduleItem('three', 3.39, 3)
print(item3)

print("-")


items = OrderedDict([(item1.name, item1), (item2.name, item2), (item3.name, item3)])
print(items)
print("-")

schedule = Schedule(items)
print(schedule)
print("-")

item = schedule.item('one')
print('name: %s: %s' % ('one', item))

item = schedule.item('x')
print('name: %s: %s' % ('x', item))

print("-")


jstr = JSONify.dumps(schedule)

print(jstr, file=sys.stderr)
print("-")


jdict = json.loads(jstr)

schedule = Schedule.construct_from_jdict(jdict)
print(schedule)
