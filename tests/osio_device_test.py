#!/usr/bin/env python3

'''
Created on 7 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
{"msg": null, "err": {"code": "UNKNOWN_CMD", "value": "hello"}}
{"msg": {"op": "scs-rpi-006", "spec": "scs-rpi-006"}, "err": null}
'''

import json


from scs_core.common.json import JSONify

from scs_core.osio.data.device import Device
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

location = Location(50.819456, -0.128330, 10, None, "BN2 1AF")

name = "scs-rpi-006"
description = "South Coast Science Raspberry Pi development platform for BB"

password = "science123"
password_is_locked = False

device_type = "Alpha Pi Eng."
batch = ""

org_id = "south-coast-science-dev"
owner_id = "southcoastscience-dev"

tags = ["temperature", "humidity", "NO", "NO2", "CO", "O3", "PM1", "PM2.5", "PM10"]


# --------------------------------------------------------------------------------------------------------------------

print(location)
print("-")

device = Device(None, name, description, password, password_is_locked, location, device_type, batch, org_id, owner_id, tags)
print(device)
print("-")

jdict = device.as_json()
print(jdict)
print("-")

jstr = JSONify.dumps(jdict)
print(jstr)
print("=")


# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr)
print(jdict)
print("-")

device = Device.construct_from_jdict(jdict)
print(device)
print("-")

location = device.location
print(location)
print("-")
