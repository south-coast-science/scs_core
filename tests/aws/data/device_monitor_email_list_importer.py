#!/usr/bin/env python3

"""
Created on 14 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client

from scs_core.aws.data.email_list import EmailList
from scs_core.aws.data.device_monitor_email_list import DeviceMonitorEmailList

from scs_core.aws.manager.s3_manager import S3PersistenceManager

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# ------------------------------------------------------------------------------------------------------------
# resources...

if not AccessKey.exists(Host):
    print("device_monitor: access key not available", file=sys.stderr)
    exit(1)

try:
    key = AccessKey.load(Host, encryption_key=AccessKey.password_from_user())
except (KeyError, ValueError):
    print("device_monitor: incorrect password", file=sys.stderr)
    exit(1)

client = Client.construct('s3', key)
resource_client = Client.resource('s3', key)

# S3PersistenceManager...
persistence_manager = S3PersistenceManager(client, resource_client)


# --------------------------------------------------------------------------------------------------------------------

imported = EmailList.load(persistence_manager)

device_dict = {}
for device_tag, recipients in imported.email_list.items():
    if recipients is None:
        email_list = set()
    elif isinstance(recipients, list):
        email_list = set(recipients)
    else:
        email_list = {recipients}

    device_dict[device_tag] = email_list

device_email_list = DeviceMonitorEmailList(device_dict)
print(JSONify.dumps(device_email_list))
print("-")

device_email_list.save(persistence_manager)

# device_email_list = DeviceMonitorEmailList.load(persistence_manager)
# print(JSONify.dumps(device_email_list))
# print("-")
