#!/usr/bin/env python3

"""
Created on 7 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
{"msg": null, "err": {"code": "UNKNOWN_CMD", "value": "hello"}}
{"msg": {"op": "scs-rpi-006", "spec": "scs-rpi-006"}, "err": null}
"""

import json

from scs_core.data.json import JSONify
from scs_core.monitor.monitor_error import MonitorError
from scs_core.monitor.monitor_request import MonitorRequest
from scs_core.monitor.monitor_response import MonitorResponse


# --------------------------------------------------------------------------------------------------------------------

request_jstr = '{"grp": "wifi", "cmd": "station", "params": ["list"]}'
print(request_jstr)
print("-")

request_jdict = json.loads(request_jstr)
print(request_jdict)
print("-")

request = MonitorRequest.construct_from_jdict(request_jdict)
print(request)
print("=")


error = MonitorError(MonitorError.CODE_UNKNOWN_CMD, "hello")
print(error)
print("-")

error_jdict = error.as_json()
print(error_jdict)
print("-")

error_jstr = JSONify.dumps(error_jdict)
print(error_jstr)
print("=")


response = MonitorResponse("bye", error)
print(error)
print("-")

response_jdict = response.as_json()
print(response_jdict)
print("-")

response_jstr = JSONify.dumps(response_jdict)
print(response_jstr)
print("=")
