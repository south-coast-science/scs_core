#!/usr/bin/env python3

"""
Created on 24 Mar 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.modem import SIM


# --------------------------------------------------------------------------------------------------------------------
# run...

lines = [
    'sim.dbus-path                             : /org/freedesktop/ModemManager1/SIM/0',
    'sim.properties.imsi                       : 234104886708667',
    'sim.properties.iccid                      : 8944110068256270054',
    'sim.properties.operator-code              : 23410',
    'sim.properties.operator-name              : giff gaff',
    'sim.properties.emergency-numbers.length   : 2',
    'sim.properties.emergency-numbers.value[1] : 999',
    'sim.properties.emergency-numbers.value[2] : 00112'
]

sim = SIM(123, 456, '789 012', 'giff gaff')
print(sim)

jstr = JSONify.dumps(sim)
print(jstr)
print("-")

sim = SIM.construct_from_jdict(json.loads(jstr))
print(sim)
print("-")

sim = SIM.construct_from_mmcli(lines)
print(sim)
