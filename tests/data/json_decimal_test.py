#!/usr/bin/env python3

"""
Created on 30 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""
import json

from decimal import Decimal
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"test-interval": null, "upper-threshold": 255.0, "lower-threshold": 5.0, "suspended": false, ' \
       '"alert-on-none": false, "topic": "south-coast-science-demo/brighton/loc/1/particulates", "field": "pm1", ' \
       '"id": 18, "cc-list": "jadempage@outlook.com, jadempage96@gmail.com", "aggregation-period": null, ' \
       '"creator-email-address": "jade.page@southcoastscience.com"}'
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

print(JSONify.dumps(jdict))
print("==")

jdict['id'] = Decimal("18")
print(jdict)
print("-")

jdict['upper-threshold'] = Decimal("255.0")
print(jdict)
print("-")

print(JSONify.dumps(jdict))

