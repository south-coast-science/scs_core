"""
Created on 22 Feb 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import sys

from scs_core.estate.mqtt_device_poller import MQTTDevicePoller
from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.client.client import Client
from scs_core.aws.manager.s3_manager import S3Manager
from scs_host.sys.host import Host

auth = APIAuth.load(Host)

# ------------------------------------------------------------------------------------------------------------
# resources...

key = None

if not AccessKey.exists(Host):
    print("aws_bucket: access key not available.", file=sys.stderr)
    exit(1)

try:
    key = AccessKey.load(Host, encryption_key=AccessKey.password_from_user())
except (KeyError, ValueError):
    print("aws_bucket: incorrect password.", file=sys.stderr)
    exit(1)

client = Client.construct('s3', key)
resource_client = Client.resource('s3', key)
dynamo_client = Client.construct('dynamodb', key)
dynamo_resource = Client.resource('dynamodb', key)

# S3Manager...
manager = S3Manager(client, resource_client)

reporter = MQTTDevicePoller(manager, dynamo_client, dynamo_resource)
reporter.update_configs()

