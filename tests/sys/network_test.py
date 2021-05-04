#!/usr/bin/env python3

"""
Created on 2 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DEVICE    TYPE      STATE      CONNECTION
eth0      ethernet  connected  Ethernet eth0
cdc-wdm0  gsm       connected  giffgaff
sit0      iptunnel  unmanaged  --
lo        loopback  unmanaged  --
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.network import Networks

# --------------------------------------------------------------------------------------------------------------------
# run...

lines = [
    'DEVICE    TYPE      STATE      CONNECTION',
    'eth0      ethernet  connected  Ethernet eth0',
    'cdc-wdm0  gsm       connected  giffgaff',
    'lo        loopback  unmanaged'
]

networks1 = Networks.construct_from_nmcli(lines)
print(networks1)

jstr = JSONify.dumps(networks1)
print(jstr)
print("-")

networks2 = Networks.construct_from_jdict(json.loads(jstr))
print(networks2)
print("-")

print(networks2 == networks1)
