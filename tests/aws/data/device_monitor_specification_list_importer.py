#!/usr/bin/env python3

"""
Created on 14 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client

from scs_core.aws.manager.s3_manager import S3PersistenceManager

from scs_core.aws.monitor.device.device_monitor_specification import DeviceMonitorSpecification, \
    DeviceMonitorSpecificationList

from scs_core.aws.monitor.device.device_monitor_email_list import DeviceMonitorEmailList

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# ------------------------------------------------------------------------------------------------------------
# resources...

if not AccessKey.exists(Host):
    print("device_monitor: access key not available", file=sys.stderr)
    exit(1)

try:
    key = AccessKey.load(Host, encryption_key='beloff')     # AccessKey.password_from_user()
except (KeyError, ValueError):
    print("device_monitor: incorrect password", file=sys.stderr)
    exit(1)

client = Client.construct('s3', key)
resource_client = Client.resource('s3', key)

# S3PersistenceManager...
persistence_manager = S3PersistenceManager(client, resource_client)


# --------------------------------------------------------------------------------------------------------------------

device_email_list = DeviceMonitorEmailList.load(persistence_manager)

device_dict = {}
for device_tag, email_list in device_email_list.device_dict.items():
    specification = DeviceMonitorSpecification(device_tag, set(email_list), False)
    device_dict[device_tag] = specification

device_specification_list = DeviceMonitorSpecificationList(device_dict)
device_specification_list.save(persistence_manager)

print(device_specification_list)
print("-")

device_specification_list = DeviceMonitorSpecificationList.load(persistence_manager)
print(JSONify.dumps(device_specification_list))

