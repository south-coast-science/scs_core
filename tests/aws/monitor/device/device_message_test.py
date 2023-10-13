#!/usr/bin/env python3

"""
Created on 12 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.monitor.device.device_monitor_report import DeviceStatusChange, DeviceMonitorMessage, \
    DeviceMonitorReport

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

device_tag = 'scs-be2-3'

with open('device_monitor_report.json') as f:
    report = DeviceMonitorReport.construct_from_jdict(json.load(f))

status = report.device(device_tag)
print(status)
print("=")

message = DeviceMonitorMessage.construct(status, DeviceStatusChange.CAUSE_OFFLINE)
print(message)
print("-")

print(message.subject())
print("-")

print(JSONify.dumps(message))
print("-")

message = DeviceMonitorMessage.construct(status, DeviceStatusChange.CAUSE_TOPIC_INACTIVE, topic='test/topic')
print(message)
print("-")

print(message.subject())
print("-")

print(JSONify.dumps(message))
print("-")
