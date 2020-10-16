"""
Created on 02 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)
"""


import json

from scs_core.aws.monitor.scs_device import SCSDevice
from scs_core.aws.manager.s3_manager import S3Manager


class DeviceListManager(object):
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client, device_monitor_conf):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__client = client
        self.__resource_client = resource_client

    # ----------------------------------------------------------------------------------------------------------------

    def add_device(self, device_tag, device_emails):
        bucket_manager = S3Manager(self.__client, self.__resource_client)
        data = bucket_manager.retrieve_from_bucket(self.__config.bucket_name, self.__config.resource_name)
        if "," in device_emails:
            emails = device_emails.split(",")
        else:
            emails = json.dumps(device_emails)
        new_dev = SCSDevice(device_tag, emails, None, None, None).as_json()
        new_dev_json = dict(new_dev)
        json_data = json.loads(data)
        json_data.append(new_dev_json)
        data_string = json.dumps(json_data)
        data_string.encode()
        bucket_manager.upload_bytes_to_bucket(self.__config.bucket_name, data_string, self.__config.resource_name)
        return data_string

    def add_device_from_json(self, json_string):
        bucket_manager = S3Manager(self.__client, self.__resource_client)
        data = bucket_manager.retrieve_from_bucket(self.__config.bucket_name, self.__config.resource_name)
        json_data = json.loads(data)
        new_json_data = json.loads(json_string)
        for line in new_json_data:
            new_dev = SCSDevice(line['dev-tag'], line['email'], None, None, None).as_json()
            new_dev_json = dict(new_dev)
            json_data.append(new_dev_json)
        data_string = json.dumps(json_data)
        data_string.encode()
        bucket_manager.upload_bytes_to_bucket(self.__config.bucket_name, data_string, self.__config.resource_name)
        return data_string

    def list_current_devices(self):
        bucket_manager = S3Manager(self.__client, self.__resource_client)
        data = bucket_manager.retrieve_from_bucket(self.__config.bucket_name, self.__config.resource_name)
        return data
