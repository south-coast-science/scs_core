#!/usr/bin/env python3

"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.conf import Conf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf1 = Conf.load(Host)
print(conf1)
print("-")

# TODO: save

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("===")

conf2 = Conf.construct_from_jdict(json.loads(jstr))
print(conf2)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("-")

equals = conf1 == conf2

print("equals: %s" % equals)
