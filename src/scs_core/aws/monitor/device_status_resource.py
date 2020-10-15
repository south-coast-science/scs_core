"""
Created on 08 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)
"""
import json

import boto3

from scs_core.aws.manager.s3_manager import S3Manager


class S3DeviceStatusList(object):
    __BUCKET_NAME = "scs-device-monitor"
    __RESOURCE_NAME = "device_status_list"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client):
        """
        Constructor
        """
        self.__resource_client = resource_client
        self.__client = client
        self.__previous_device_status_list = None
        self.__aws_client = boto3.client('s3', region_name="us-west-2")
        self.__aws_resource_client = boto3.resource('s3', region_name="us-west-2")

    # ----------------------------------------------------------------------------------------------------------------

    def get_device_status_list(self):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        res = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME)
        return res

    def recreate_device_status_list(self, device_list):
        last_pub = None
        device_status_list = {}
        for device in device_list:
            if device.latest_pub is not None:
                last_pub = device.latest_pub.as_json()
            device_status_list[device.device_tag] = device.is_active
        print(device_status_list)
        s3_manager = S3Manager(self.__client, self.__resource_client)
        body = json.dumps(device_status_list).encode('utf-8')
        s3_manager.put_object(self.__BUCKET_NAME, body, self.__RESOURCE_NAME)
        # Send to the bucket
