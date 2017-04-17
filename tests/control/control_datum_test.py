#!/usr/bin/env python3

"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.control.control_datum import ControlDatum
from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

serial = '00000000cda1f8b9'
now = LocalizedDatetime.now()

datum = ControlDatum.construct('cmd-1', now, 'shutdown', ['now'], serial)
print(datum)
print("-")

jstr = JSONify.dumps(datum)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

datum = ControlDatum.construct_from_jdict(jdict)
print(datum)
print("-")

valid = datum.is_valid(serial)
print("valid: %s" % valid)
print("-")

valid = datum.is_valid('00000000cda1f8b8')
print("valid: %s" % valid)
print("-")
