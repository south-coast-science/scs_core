#!/usr/bin/env python3

"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import time

from scs_core.control.command import Command
from scs_core.control.control_datum import ControlDatum
from scs_core.control.control_receipt import ControlReceipt

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

key = '00000000cda1f8b9'
now = LocalizedDatetime.now().utc()

datum = ControlDatum.construct('my-laptop', 'scs-ap1-6', now, ['test'], 20, key)
print(datum)
print("-")

jstr = JSONify.dumps(datum)
print(jstr)
print("-")

jdict = json.loads(jstr)

datum = ControlDatum.construct_from_jdict(jdict)
print(datum)
print("-")

valid = datum.is_valid(key)
print("datum valid: %s" % valid)

valid = datum.is_valid('00000000cda1f8b8')
print("datum valid: %s" % valid)
print("=")

time.sleep(1)
now = LocalizedDatetime.now().utc()

command = Command('CMD', [], return_code=0)

receipt = ControlReceipt.construct_from_datum(datum, now, command, key)
print(receipt)
print("-")

jstr = JSONify.dumps(receipt)
print(jstr)
print("-")

jdict = json.loads(jstr)

receipt = ControlReceipt.construct_from_jdict(jdict)
print(receipt)
print("-")

valid = receipt.is_valid(key)
print("receipt valid: %s" % valid)

valid = receipt.is_valid('00000000cda1f8b8')
print("receipt valid: %s" % valid)
print("-")
