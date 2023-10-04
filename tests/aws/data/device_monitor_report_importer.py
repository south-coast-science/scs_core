#!/usr/bin/env python3

"""
Created on 18 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client

from scs_core.aws.monitor.device.status_list import StatusList
from scs_core.aws.monitor.device.power_list import PowerList
from scs_core.aws.monitor.device.uptime_list import UptimeList

from scs_core.aws.manager.byline.byline_list import BylineList

from scs_core.aws.manager.s3_manager import S3PersistenceManager

from scs_core.aws.monitor.device.device_monitor_report import DeviceMonitorReport, DeviceReport, DeviceStatus, \
    TopicStatus, DeviceUptime

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta

from scs_host.sys.host import Host


# ------------------------------------------------------------------------------------------------------------

def import_status(status):
    if not status:
        return None

    try:
        return DeviceStatus(status[0], LocalizedDatetime.construct_from_jdict(status[1]))
    except TypeError:
        return DeviceStatus(status, None)


def import_uptime(uptime_jdict):
    if not uptime_jdict:
        return None

    return DeviceUptime(Timedelta.construct_from_jdict(uptime_jdict))


def import_topic(topic_status):
    if not topic_status:
        return None

    return TopicStatus({topic: import_status(status) for topic, status in topic_status.items()})


# ------------------------------------------------------------------------------------------------------------
# resources...

if not AccessKey.exists(Host):
    print("device_monitor: access key not available", file=sys.stderr)
    exit(1)

try:
    key = AccessKey.load(Host, encryption_key=AccessKey.password_from_user())     # AccessKey.password_from_user()
except (KeyError, ValueError):
    print("device_monitor: incorrect password", file=sys.stderr)
    exit(1)

client = Client.construct('s3', key)
resource_client = Client.resource('s3', key)

# S3PersistenceManager...
persistence_manager = S3PersistenceManager(client, resource_client)


# --------------------------------------------------------------------------------------------------------------------

status_list = StatusList.load(persistence_manager)
# print(status_list)
# print("-")

uptime_list = UptimeList.load(persistence_manager)
# print(uptime_list)
# print("-")

byline_list = BylineList.load(persistence_manager)
# print(byline_list)
# print("-")

power_list = PowerList.load(persistence_manager)
# print(power_list)
# print("-")


# --------------------------------------------------------------------------------------------------------------------

device_dict = {}

for device_tag in status_list.status_list:
    availability = import_status(status_list.status_list[device_tag])
    data = import_topic(byline_list.byline_list[device_tag])
    power = import_status(power_list.power_list[device_tag])
    uptime = import_uptime(uptime_list.uptime_list[device_tag])

    device_dict[device_tag] = DeviceReport(device_tag, availability, data, power, uptime)

device_monitor_report = DeviceMonitorReport(device_dict)
device_monitor_report.save(persistence_manager)

device_monitor_report = DeviceMonitorReport.load(persistence_manager)

print(JSONify.dumps(device_monitor_report, indent=4))

