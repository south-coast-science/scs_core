#!/usr/bin/env python3

"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.modem import Modem


# --------------------------------------------------------------------------------------------------------------------
# run...

lines = [
    'modem.generic.device-identifier                 : 3f07553c31ce11715037ac16c24ceddcfb6f7a0b',
    'modem.generic.manufacturer                      : QUALCOMM INCORPORATED',
    'modem.generic.model                             : QUECTEL Mobile Broadband Module',
    'modem.generic.revision                          : EC21EFAR06A01M4G'
]

modem1 = Modem.construct_from_mmcli(lines)
print(modem1)

jstr = JSONify.dumps(modem1)
print(jstr)
print("-")

modem2 = Modem.construct_from_jdict(json.loads(jstr))
print(modem2)

jstr = JSONify.dumps(modem2)
print(jstr)
print("-")

print(modem1 == modem2)
