"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import os

import boto3

from scs_core.aws.client.api_auth import APIAuth

from scs_core.aws.data.device_line import DeviceLine

from scs_core.aws.manager.byline_manager import BylineManager
from scs_core.aws.manager.s3_manager import S3Manager

from scs_core.data.path_dict import PathDict
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitor(object):

    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, device_monitor_conf, host, email_client):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__watched_device_list = {}
        self.__changed_device_list = {}
        self.__email_list = PathDict()
        self.__api_auth = APIAuth.load(host)
        self.__email_client = email_client
        self.__number_changed = 0

    # ----------------------------------------------------------------------------------------------------------------

    def get_watched_device_list(self):
        # reads auth keys from environment, if you want it to be used externally programmatically (not as a lambda)
        # this will probably need to be changed
        aws_client = boto3.client('s3', region_name=self.__config.aws_region)
        aws_resource_client = boto3.resource('s3', region_name=self.__config.aws_region)
        bucket_manager = S3Manager(aws_client, aws_resource_client)
        data = bucket_manager.retrieve_from_bucket(self.__config.bucket_name, self.__config.resource_name)

        iterator = 0
        for line in data:
            temp = DeviceLine.construct_from_jdict(line)
            if temp.email_list:
                # If no one is assigned to receive e-mail alerts, don't check
                self.__watched_device_list[iterator] = temp
                iterator += 1


    def get_changed_devices_list(self):
        for key in self.__watched_device_list:
            this_dev = self.__watched_device_list[key]
            device_data = self.get_byline_data(this_dev.device_tag)
            latest_activity = self.get_latest_response(device_data)
            if self.is_unresponsive(latest_activity):
                if this_dev.status_active:
                    this_dev.dm_status = "inactive"
                    self.__changed_device_list[self.__number_changed] = this_dev
                    self.__number_changed += 1
                this_dev.status_active = False
            else:
                if not this_dev.status_active:
                    this_dev.dm_status = "active"
                    self.__changed_device_list[self.__number_changed] = this_dev
                    self.__number_changed += 1
                this_dev.status_active = True

    def send_email_alerts(self):
        iterations = 0
        while iterations < self.__number_changed:
            this_dev = self.__changed_device_list[iterations]
            recipients = this_dev.email_list

            message = self.generate_email_message(this_dev)
            for recipient in recipients:
                self.__email_client.send_email(recipient, message)
            iterations += 1

    def get_byline_data(self, device_tag):
        manager = BylineManager(self.__api_auth)
        res = manager.find_bylines_for_device(device_tag)
        return res.as_json()


    def is_unresponsive(self, latest_pub_iso):
        latest_pub = LocalizedDatetime.construct_from_iso8601(latest_pub_iso)

        if latest_pub is None:
            return True

        now = LocalizedDatetime.now()
        delta = now - latest_pub

        return delta.minutes > self.__config.unresponsive_minutes_allowed

    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_latest_response(byline_data):
        cur_latest = None
        for byline in byline_data["bylines"]:
            j_byline = byline.as_json()
            latest = j_byline["pub"]
            if latest is not None:
                if cur_latest is None:
                    cur_latest = latest
                else:
                    if latest > cur_latest:
                        cur_latest = latest
        return cur_latest

    @staticmethod
    def generate_email_message(device):
        old_status = "active" if not device.status_active else "inactive"
        if device.dm_status == "active" or "inactive":
            template = "status_changed.txt"
        else:
            template = None
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', template)
        f = open(filepath, "r")
        message = f.read()
        message = (message.replace("DEVICE_NAME", device.device_tag))
        message = (message.replace("LAST_CHECK_TIME", device.last_checked))
        message = (message.replace("OLD_STATUS", old_status))
        message = (message.replace("NEW_STATUS", device.dm_status))
        message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))
        return message

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "device_monitor:{unresponsive_minutes_allowed:%s, watched_device_list:%s, " \
               "changed_device_list:%s, number_changed:%s }" % \
               (self.__config.unresponsive_minutes_allowed, self.__watched_device_list, self.__changed_device_list,
                self.__number_changed)
