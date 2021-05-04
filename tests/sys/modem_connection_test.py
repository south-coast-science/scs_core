#!/usr/bin/env python3

"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.modem import ModemConnection


# --------------------------------------------------------------------------------------------------------------------
# run...

lines = [
    'modem.generic.state                            : connected',
    'modem.generic.state-failed-reason              : --',
    'modem.generic.signal-quality.value             : 67',
    'modem.generic.signal-quality.recent            : yes'
]

connection1 = ModemConnection.construct_from_mmcli(lines)
print(connection1)

jstr = JSONify.dumps(connection1)
print(jstr)
print("-")

connection2 = ModemConnection.construct_from_jdict(json.loads(jstr))
print(connection2)

jstr = JSONify.dumps(connection2)
print(jstr)
print("-")

print(connection1 == connection2)
