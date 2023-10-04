#!/usr/bin/env python3

"""
Created on 14 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.monitor.device.device_monitor_email_list import DeviceMonitorEmailList


# ------------------------------------------------------------------------------------------------------------
# resources...

device_list = DeviceMonitorEmailList({})
print(device_list)

device_list.add('scs-abc-1', 'test@a.com')
print(device_list)

device_list.add('scs-abc-1', 'test@b.com')
print(device_list)

device_list.add('scs-abc-2', 'test@a.com')
print(device_list)
print("-")

print(device_list.subset('test@a.com'))
print(device_list.subset('test@b.com'))
print("-")

device_list.discard(None, 'test@a.com')
device_list.discard(None, 'test@a.com')
print(device_list)
print("-")

print(device_list.subset('test@a.com'))
print("-")

# TODO: check load / save
