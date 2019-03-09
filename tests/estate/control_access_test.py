#!/usr/bin/env python3

"""
Created on 9 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.estate.control_access import ControlAccess, ControlAccessSet

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

print("device1...")
device1 = ControlAccess("scs-rpi-006", "scs-ap1-6", "secret2",
                        "south-coast-science-dev/development/device/alpha-pi-eng-000006/control")
print(device1)
print("-")

print("group...")
devices = {device1.hostname: device1}
print(devices)

group = ControlAccessSet(devices)
print(group)
print("-")

print("device2...")
device2 = ControlAccess("scs-bbe-002", "scs-be2-2", "secret1",
                        "south-coast-science-dev/production-test/device/alpha-bb-eng-000002/control")
print(device2)
print("-")

print("append...")
group.insert(device2)

jstr = JSONify.dumps(group)

print(jstr)
print("-")

print("remake...")
group = ControlAccessSet.construct_from_jdict(json.loads(jstr))
print(group)
print("-")

print("save...")
group.save(Host)

print("load...")
group = ControlAccessSet.load(Host)
print(group)
print("-")

print("devices...")
for device in group.devices:
    print(JSONify.dumps(device))
print("-")

print("device...")
print(group.device("scs-rpi-006"))
print(group.device("scs-rpi-xxx"))
print("-")

