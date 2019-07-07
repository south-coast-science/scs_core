#!/usr/bin/env python3

"""
Created on 9 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.estate.mqtt_peer import MQTTPeer, MQTTPeerSet

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

print("auth1...")
auth1 = MQTTPeer("scs-rpi-006", "scs-ap1-6", "secret2",
                 "south-coast-science-dev/development/auth/alpha-pi-eng-000006/control")
print(auth1)
print("-")

print("group...")
auths = {auth1.hostname: auth1}
print(auths)

group = MQTTPeerSet(auths)
print(group)
print("-")

print("auth2...")
auth2 = MQTTPeer("scs-bbe-002", "scs-be2-2", "secret1",
                 "south-coast-science-dev/production-test/auth/alpha-bb-eng-000002/control")
print(auth2)
print("-")

print("append...")
group.insert(auth2)

jstr = JSONify.dumps(group)

print(jstr)
print("-")

print("remake...")
group = MQTTPeerSet.construct_from_jdict(json.loads(jstr))
print(group)
print("-")

print("save...")
group.save(Host)

print("load...")
group = MQTTPeerSet.load(Host)
print(group)
print("-")

print("auths...")
for auth in group.auths:
    print(JSONify.dumps(auth))
print("-")

print("auth...")
print(group.auth("scs-rpi-006"))
print(group.auth("scs-rpi-xxx"))
print("-")

