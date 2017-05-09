#!/usr/bin/env python3

"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import time

from collections import OrderedDict

from scs_core.control.control_datum import ControlDatum
from scs_core.control.control_receipt import ControlReceipt
from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

serial = '00000000cda1f8b9'
now = LocalizedDatetime.now()

datum = ControlDatum.construct('my-laptop', 'scs-ap1-6', now, ['now'], serial)
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
print("datum valid: %s" % valid)

valid = datum.is_valid('00000000cda1f8b8')
print("datum valid: %s" % valid)
print("=")

time.sleep(1)
now = LocalizedDatetime.now()

receipt = ControlReceipt.construct_from_datum(datum, now, serial)
print(receipt)
print("-")

jstr = JSONify.dumps(receipt)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

receipt = ControlReceipt.construct_from_jdict(jdict)
print(receipt)
print("-")

valid = receipt.is_valid(serial)
print("receipt valid: %s" % valid)

valid = receipt.is_valid('00000000cda1f8b8')
print("receipt valid: %s" % valid)
print("-")
