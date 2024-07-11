#!/usr/bin/env python3

"""
Created on 10 Jun 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.device_tag import DeviceTag


# --------------------------------------------------------------------------------------------------------------------

device_tag_1 = DeviceTag('scs', 'opc', 1)
print("device_tag_1: %s" % device_tag_1)

jstr_1 = JSONify.dumps(device_tag_1)
print("jstr_1: %s" % jstr_1)

jstr_1 = JSONify.dumps(device_tag_1, sortable=True)
print("jstr_1: %s" % jstr_1)
print("-")

device_tag_2 = DeviceTag.construct_from_jdict(json.loads(jstr_1))
print("device_tag_2: %s" % device_tag_2)

equals = device_tag_1 == device_tag_2
print("equals: %s" % equals)
print("-")

is_valid = DeviceTag.is_valid("scs-opc-1")
print("is_valid: %s" % is_valid)

is_valid = DeviceTag.is_valid("scs-opc-a")
print("is_valid: %s" % is_valid)

d = {device_tag_1: 'a'}
print(d)
print("-")

device_tag_3 = DeviceTag.construct_from_jdict('bruno')
print("device_tag_2: %s" % device_tag_3)

d = {device_tag_3: 'a'}
print(d)
