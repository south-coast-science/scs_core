#!/usr/bin/env python3

"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf1 = Configuration.load(Host)
print(conf1)
print("-")

conf1.save(Host)
conf1 = Configuration.load(Host)
print(conf1)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("===")

conf2 = Configuration.construct_from_jdict(json.loads(jstr))
print(conf2)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("-")

equals = conf1 == conf2

print("equals: %s" % equals)