"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3

from scs_core.aws.manager.device_list_manager import DeviceListManager
from scs_core.aws.monitor.device_monitor_conf import DeviceMonitorConf

aws_client = boto3.client('s3', region_name="us-west-2")
aws_resource_client = boto3.resource('s3', region_name="us-west-2")

dmc = DeviceMonitorConf().load_from_cloud(aws_client, aws_resource_client)
dlm = DeviceListManager(aws_client, aws_resource_client, dmc)
# dlm.add_device("some-dev-tag", "abcdefg@mail.com")
# dlm.add_device("some-dev-tag", "abcdefg@mail.com,hello@inbox.com,someuser@somemail.com")
json_string = "[{\"dev-tag\":\"TEST-EMAIL-2\",\"email\":[" \
              "\"abcdefg@mail.com\",\"hello@inbox.com\",\"someuser@somemail.com\"]}] "
dlm.add_device_from_json(json_string)
