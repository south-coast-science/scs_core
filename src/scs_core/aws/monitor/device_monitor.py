"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os
from collections import OrderedDict

from scs_core.aws.manager.s3_manager import S3Manager

from scs_core.data.timedelta import Timedelta

from scs_core.aws.client.api_auth import APIAuth

from scs_core.aws.manager.byline_manager import BylineManager

from scs_core.aws.monitor.device_tester import DeviceTester
from scs_core.aws.monitor.scs_device import SCSDevice

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitor(object):
    __RUN_FREQUENCY_MINUTES = 60
    __BUCKET_NAME = "scs-device-monitor"
    __RESOURCE_NAME_STATUS = "device_status_list"
    __RESOURCE_NAME_UPTIME = "device_uptime_list"

    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, device_monitor_conf, email_client, client, resource_client, host=None):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__api_auth = APIAuth.load(host) if host else None
        self.__email_client = email_client
        self.__client = client
        self.__resource_client = resource_client

    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        # Get resources
        s3_manager = S3Manager(self.__client, self.__resource_client)
        device_statuses = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_STATUS)
        device_uptimes = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)

        device_list = self.get_devices_by_byline()

        # Do all tests
        iterating = 0
        email_sent = False
        while iterating < len(device_list):
            this_dev = device_list[iterating]
            self.get_latest_pubs(this_dev)

            device_tester = DeviceTester(this_dev, self.__config, self.__api_auth)
            # Check if device has stopped/started reporting
            if device_tester.is_inactive():
                this_dev.is_active = False
            else:
                this_dev.is_active = True
            if device_tester.has_status_changed(device_statuses):
                this_dev.dm_status = "activity_change"
                self.generate_email(this_dev)
                email_sent = True

            # see if all topics are published on recently
            inactive, byline = device_tester.is_publishing_on_all_channels()
            if inactive:
                topic = byline.topic
                this_dev.dm_status = "byline"
                if not email_sent:
                    self.generate_email(this_dev, topic)
                    email_sent = True

            # check if rebooted
            if device_tester.was_rebooted(device_uptimes):
                this_dev.dm_status = "reboot"
                if not email_sent:
                    self.generate_email(this_dev)
                    email_sent = True

            # TODO test for null values for each topic
            iterating += 1
        # TODO save back to bucket
        self.recreate_uptime_list(device_list)


    def send_email_alert(self, this_dev, message):
        recipients = this_dev.email_list
        if recipients is None:
            recipients = self.__config.email_name
        else:
            recipients = this_dev.email_list + self.__config.email_name
        for recipient in recipients:
            pass
            # self.__email_client.send_email(recipient, message) commented out so I don't get spammed whilst developing

    def get_devices_by_byline(self):
        # TODO change with direct call to lambda ARN
        device_list = []
        manager = BylineManager(self.__api_auth)
        group = manager.find_bylines_for_topic("", "/control")
        for device in group.devices:
            device_bylines = group.bylines_for_device(device)
            temp = SCSDevice(device, None, False, device_bylines)
            device_list.append(temp)
        return device_list

    def generate_email(self, device, byline_topic=None):
        message = ""
        template = None
        old_status = "active" if not device.is_active else "inactive"

        # Get templates
        if device.dm_status == "activity_change":
            template = "status_changed.txt"
        elif device.dm_status == "byline":
            template = "byline_inactive.txt"
        elif device.dm_status == "reboot":
            template = "uptime.txt"

        # Load template
        if template:
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', template)
            f = open(filepath, "r")
            message = f.read()
        else:
            return

        # Replace for specific device
        message = (message.replace("DEVICE_NAME", device.device_tag))
        message = (message.replace("LAST_CHECK_TIME", self.get_last_run_time()))
        message = (message.replace("OLD_STATUS", old_status))
        message = (message.replace("NEW_STATUS", device.dm_status))
        message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))
        message = (message.replace("TOPIC_NAME", byline_topic if byline_topic else ""))
        message = (message.replace("TIME_DELTA", str(self.__config.unresponsive_minutes_allowed)))
        message = (message.replace("NOW_UPTIME", device.uptime.as_json() if device.uptime else ""))
        self.send_email_alert(device, message)

    def get_last_run_time(self):
        now = LocalizedDatetime.now()
        td = Timedelta(minutes=self.__RUN_FREQUENCY_MINUTES)
        res = now - td
        return res.as_json()

    def recreate_status_list(self, status_list):
        pass

    def recreate_uptime_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            data = (device.as_uptime_json())
            json_data[data["dev-tag"]] = data["uptime"]

        s3_manager.upload_bytes_to_bucket(json_data, self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)


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

    # def __str__(self, *args, **kwargs):
    #     return "device_monitor:{unresponsive_minutes_allowed:%s, " \
    #            "changed_device_list:%s }" % \
    #            (self.__config.unresponsive_minutes_allowed,
    #             self.__changed_device_list)
