#!/usr/bin/env python3

"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.diurnal_period import DiurnalPeriod
from scs_core.data.json import JSONify
from scs_core.data.recurring_period import RecurringPeriod

from scs_core.estate.baseline_conf import BaselineConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

name = 'test'

timezone_str = 'Europe/London'
start_time_str = '17:00'
end_time_str = '8:00'
interval = 5

sample_period = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)
aggregation_period = RecurringPeriod.construct(interval, 'M', timezone_str)

minimums = {'CO': 200, 'CO2': 420, 'H2S': 5, 'NO': 10, 'NO2': 10, 'SO2': 5}      # 'Ox': 50,

conf = BaselineConf(name, sample_period, aggregation_period, minimums)
print(conf)
print("-")

jstr = JSONify.dumps(conf)
print(jstr)
print("-")

conf.save(Host)

print("loading...")
conf = BaselineConf.load(Host, name=name)
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
