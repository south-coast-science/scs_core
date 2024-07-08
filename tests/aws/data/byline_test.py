#!/usr/bin/env python3

"""
Created on 22 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.aws.manager.byline.byline import Byline

# --------------------------------------------------------------------------------------------------------------------

jdict =  {
       'last_write': '2020-10-23T08:35:20Z',
       'message': {'val': {'hmd': 70.6, 'tmp': 19.3, 'bar': None}, 'rec': '2020-10-23T08:35:20Z', 'tag': 'scs-bgx-401'},
       'topic': 'south-coast-science-demo/brighton/loc/1/climate',
       'rec': '2020-10-23T08:35:20Z',
       'lastSeenTime': '2020-10-23T08:35:39.113Z',
       'device': 'scs-bgx-401'}

print(jdict)
print("-")

byline = Byline.construct_from_jdict(jdict)
print(byline)
print("-")

message = byline.message
print("message: %s" % message)
print("-")

jdict = json.loads(message)
print("message jdict: %s" % jdict)
print("=")

jstr = JSONify.dumps(byline)
print("byline jstr: %s" % jstr)
print("-")

jdict = json.loads(jstr)
print("byline jdict: %s" % jdict)
print("-")

byline = Byline.construct_from_jdict(jdict)
print(byline)
print("-")

message = byline.message
print("message: %s" % message)
print("-")

jdict = json.loads(message)
print("message jdict: %s" % jdict)
print("=")
