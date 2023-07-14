#!/usr/bin/env python3

"""
Created on 12 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.diurnal_period import DiurnalPeriod

from scs_core.estate.baseline_conf import BaselineConf
from scs_core.estate.baseline_conf_old import BaselineConf as OldBaselineConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

names = [
    'athens',
    'costa_rica',
    'freshfield',
    'heathrow',
    'preston_circus',
    'vitoria'
]

for name in names:
    old_conf = OldBaselineConf.load(Host, name)
    print("old_conf: %s" % old_conf)

    start_time_str = str(old_conf.start_hour) + ':00:00'
    end_time_str = str(old_conf.end_hour) + ':00:00'
    timezone_str = old_conf.timezone

    sample_period = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)

    new_conf = BaselineConf(old_conf.name, sample_period, old_conf.aggregation_period, old_conf.minimums)
    new_conf.save(Host)

    print("new_conf: %s" % new_conf)
    print("-")
