#!/usr/bin/env python3

"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.recurring_period import RecurringMinutes

from scs_core.estate.baseline_conf import BaselineConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

lab_timezone = 'Europe/London'
start_hour = 23
end_hour = 8
aggregation_period = RecurringMinutes(5)
gas_offsets = {'NO': 10, 'CO': 300}

conf = BaselineConf(lab_timezone, start_hour, end_hour, aggregation_period, gas_offsets)
print(conf)
print("-")

jstr = JSONify.dumps(conf)
print(jstr)
print("-")

conf = BaselineConf.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

conf.save(Host)
conf = BaselineConf.load(Host)
print(conf)
print("=")

origin = LocalizedDatetime.now()
print("origin: %s" % origin)

start_datetime = conf.start_datetime(origin)
print("start_datetime: %s" % start_datetime)

end_datetime = conf.end_datetime(origin)
print("end_datetime: %s" % end_datetime.utc())
print("=")

checkpoint = conf.checkpoint()
print("checkpoint: %s" % checkpoint)
