#!/usr/bin/env python3

"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
{"msg": null, "err": {"code": "UNKNOWN_CMD", "value": "hello"}}
{"msg": {"op": "scs-rpi-006", "spec": "scs-rpi-006"}, "err": null}
"""

import json

from scs_core.data.json import JSONify
from scs_core.osio.data.topic import Topic


# --------------------------------------------------------------------------------------------------------------------

topic_jstr = '''  {
    "description": "GPS location, fix level, SIV, HDOP, max S/N and average S/N",
    "stats": {
      "period": 0,
      "last-reading": "137 days ago",
      "contributors": [
        {
          "name": "Air Connector",
          "id": "air-connector",
          "gravatar-hash": "c8470ac52266e3ff56e4bb8a3b66fd5c"
        }
      ],
      "last-location": {
        "lat": 51.525305,
        "lon": -0.135455
      }
    },
    "unit": "degrees, degrees, 0-3, -, -, decibels (dB), decibels (dB)",
    "name": "GPS @ Air / 2015205",
    "public": true,
    "topic": "/orgs/south-coast-science-dev/air-te-v2/2015205/location",
    "bookmark-count": 0,
    "topic-info": {
      "format": "application/json",
      "graph-path": "datum.avg-snr"
    }
  }'''

print(topic_jstr)
print("-")

topic_jdict = json.loads(topic_jstr)
print(topic_jdict)
print("-")

topic = Topic.construct_from_jdict(topic_jdict)
print(topic)
print("-")

print(JSONify.dumps(topic))
print("-")
