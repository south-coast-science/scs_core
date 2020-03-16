#!/usr/bin/env python3

"""
Created on 7 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
{"msg": null, "err": {"code": "UNKNOWN_CMD", "value": "hello"}}
{"msg": {"op": "scs-rpi-006", "spec": "scs-rpi-006"}, "err": null}
"""

import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.osio.data.message_body import MessageBody
from scs_core.osio.data.message_response import MessageResponse

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

tag = "scs-ap1-0"
print(tag)
print("-")

now = LocalizedDatetime.now().utc()
print(now)
print("-")

value = "hello"
print(value)
print("-")

datum = Sample(tag, None, now, ("greeting", "hello"))
print(datum)
print("-")

body = MessageBody(datum)
print(body)
print("-")

body_jdict = body.as_json()
print(body_jdict)
print("-")

body_jstr = JSONify.dumps(body_jdict)
print(body_jstr)
print("=")


response_jstr = '{"message": "hello to you"}'
print(response_jstr)
print("-")

response_jdict = json.loads(response_jstr)
print(response_jdict)
print("-")

response = MessageResponse.construct_from_jdict(response_jdict)
print(response)
print("=")
