#!/usr/bin/env python3

"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import sys

import boto3

from scs_core.aws.client.email_client import EmailClient
from scs_core.aws.monitor.device_monitor_conf import DeviceMonitorConf
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

def run_device_monitor():
    # dm conf
    email_manager = EmailClient().default_client()
    aws_client = boto3.client('s3', region_name='us-west-2')
    aws_resource_client = boto3.resource('s3', region_name='us-west-2')

    dmc = DeviceMonitorConf().load_from_cloud(aws_client, aws_resource_client)
    if dmc is None:
        print("device_monitor: DeviceMonitorConf not available.", file=sys.stderr)
        exit(1)

    # dm...
    dm = dmc.init_device_manager(Host, email_manager)

    dm.get_watched_device_list()
    dm.get_changed_devices_list()
    dm.send_email_alerts()


# --------------------------------------------------------------------------------------------------------------------
run_device_monitor()

# monitor = DeviceMonitor(10, Host)
#
# is_unresponsive = monitor.is_unresponsive('2020-09-29T17:25:39+01:00')
# print("is_unresponsive: %s" % is_unresponsive)

# run_device_monitor(10)
