"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import os

import boto3
from scs_core.aws.manager.byline_manager import BylineManager

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.monitor.device_status_resource import S3DeviceStatusList
from scs_core.aws.monitor.device_tester import DeviceTester

from scs_core.aws.monitor.scs_device import SCSDevice

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
        self.__watched_device_list = []
        self.__changed_device_list = []
        self.__email_list = PathDict()
        self.__api_auth = APIAuth.load(host)
        self.__email_client = email_client
        self.__aws_client = boto3.client('s3', region_name=self.__config.aws_region)
        self.__aws_resource_client = boto3.resource('s3', region_name="us-west-2")
        # reads auth keys from environment, if you want it to be used externally programmatically (not as a lambda)
        # this will need to be changed

    # ----------------------------------------------------------------------------------------------------------------

    def get_watched_device_list(self):
        self.get_devices_by_byline()
        # Do e-mails

    def check_devices(self):
        s3_list = S3DeviceStatusList(self.__aws_client, self.__aws_client)
        old_device_statuses = s3_list.get_device_status_list()
        iterating = 0
        while iterating < len(self.__watched_device_list):
            this_dev = self.__watched_device_list[iterating]
            self.get_latest_pubs(this_dev)
            device_tester = DeviceTester(this_dev, self.__config)
            # Check if device has stopped/started reporting
            if device_tester.is_inactive():
                this_dev.is_active = False
            else:
                this_dev.is_active = True
            if device_tester.has_status_changed(old_device_statuses):
                this_dev.dm_status = "activity_change"
                # self.generate_email_message(this_dev)
            else:
                # see if all topics are published on recently
                inactive, byline = device_tester.is_publishing_on_all_channels()
                if inactive:
                    topic = byline.topic
                    this_dev.dm_status = "byline"
                    self.generate_email_message(this_dev, topic)
                else:
                    # do next test...
                    pass
            iterating += 1

        # Update device list on S3 when done!

    @staticmethod
    def send_email_alert(this_dev, message):
        recipients = this_dev.email_list
        if recipients is None:
            recipients = "devicetest147147@gmail.com"
        else:
            recipients = this_dev.email_list + "devicetest147147@gmail.com"
        for recipient in recipients:
            pass
            # self.__email_client.send_email(recipient, message)

    def get_devices_by_byline(self):
        manager = BylineManager(self.__api_auth)
        group = manager.find_bylines_for_topic("", "/control")
        for device in group.devices:
            device_bylines = group.bylines_for_device(device)
            temp = SCSDevice(device, None, False, device_bylines)
            self.__watched_device_list.append(temp)

    def generate_email_message(self, device, byline_topic=None):
        message = ""
        if device.dm_status == "activity_change":
            template = "status_changed.txt"
            old_status = "active" if not device.is_active else "inactive"
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', template)
            f = open(filepath, "r")
            message = f.read()
            message = (message.replace("DEVICE_NAME", device.device_tag))
            message = (message.replace("LAST_CHECK_TIME", device.last_checked))
            message = (message.replace("OLD_STATUS", old_status))
            message = (message.replace("NEW_STATUS", device.dm_status))
            message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))
        elif device.dm_status == "byline":
            template = "byline_inactive.txt"
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', template)
            f = open(filepath, "r")
            message = f.read()
            message = (message.replace("DEVICE_NAME", device.device_tag))
            message = (message.replace("LAST_CHECK_TIME", device.last_checked))
            message = (message.replace("TOPIC_NAME", byline_topic))
            message = (message.replace("TIME_DELTA", self.__config.unresponsive_minutes_allowed))
            message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))

        if message is not None:
            self.send_email_alert(device, message)

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_latest_pubs(scs_device):
        values = False
        device_bylines = scs_device.bylines
        for byline in device_bylines:
            if byline.pub is not None:
                values = True
        if values:
            latest = max([device_bylines.pub for device_bylines in device_bylines if device_bylines.pub is not None])
        else:
            latest = None
        scs_device.latest_pub = latest

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "device_monitor:{unresponsive_minutes_allowed:%s, watched_device_list:%s, " \
               "changed_device_list:%s }" % \
               (self.__config.unresponsive_minutes_allowed, self.__watched_device_list,
                self.__changed_device_list)
