#!/usr/bin/env python3

"""
Created on 14 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration


# --------------------------------------------------------------------------------------------------------------------

with open('config_test.json') as f:
    jstr = f.read().strip()

# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr)
config = Configuration.construct_from_jdict(jdict.get('val'))
print(JSONify.dumps(config, indent=4))

