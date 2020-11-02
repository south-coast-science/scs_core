"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os
import time
from collections import OrderedDict

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.manager.byline_manager import BylineManager
from scs_core.aws.manager.s3_manager import S3Manager
from scs_core.aws.monitor.device_tester import DeviceTester
from scs_core.aws.monitor.email_queue import EmailQueue
from scs_core.aws.monitor.email_queue_manager import EmailQueueManager
from scs_core.aws.monitor.scs_device import SCSDevice
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitor(object):
    __RUN_FREQUENCY_MINUTES = 60
    __BUCKET_NAME = "scs-device-monitor"
    __RESOURCE_NAME_STATUS = "device_status_list"
    __RESOURCE_NAME_UPTIME = "device_uptime_list"
    __RESOURCE_NAME_BYLINES = "device_bylines_list"

    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, device_monitor_conf, client, resource_client, email_client, host=None):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__api_auth = APIAuth.load(host) if host else None
        self.__client = client
        self.__resource_client = resource_client
        self.__email_queue = EmailQueue()
        self.__email_queue_manager = EmailQueueManager(email_client)
        self.__email_client = email_client
        self.__expected_queue_length = 0

    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        # Get resources
        s3_manager = S3Manager(self.__client, self.__resource_client)
        device_statuses = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_STATUS)
        device_uptimes = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)
        device_byline_statuses = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_BYLINES)

        device_list = self.get_devices_by_byline()

        # start eqm
        self.__email_queue_manager.start()

        # Do all tests
        iterating = 0
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
                this_dev.email_sent = True

            # see if all topics are published on recently
            device_tester.get_byline_activity()
            if not this_dev.email_sent:
                inactive, topic = device_tester.has_byline_status_changed(device_byline_statuses)
                if inactive:
                    this_dev.dm_status = "byline"
                    self.generate_email(this_dev, topic)
                    this_dev.email_sent = True

            # check for weird (null) values
            if not this_dev.email_sent:
                is_okay, field, field_type = device_tester.check_values()
                this_dev.dm_status = "values"
                if not is_okay:
                    self.generate_email(this_dev, None, field, field_type)
                    this_dev.email_sent = True

            # check if rebooted
            if device_tester.was_rebooted(device_uptimes):
                this_dev.dm_status = "reboot"
                if not this_dev.email_sent:
                    self.generate_email(this_dev)
                    this_dev.email_sent = True

            iterating += 1

        self.recreate_status_list(device_list)
        self.recreate_uptime_list(device_list)
        self.recreate_pub_list(device_list)

        # let the email queue finish...
        if self.__email_queue.queue:
            while len(self.__email_queue.queue) > 0:
                self.__email_queue = self.__email_queue_manager.get_queue()
                keys_left = len(self.__email_queue.queue)
                print("Keys left:%s" % keys_left)
                time.sleep(10)

    def cleanup(self):
        self.__email_queue_manager.stop()

    def send_email_alert(self, this_dev, message):
        self.__expected_queue_length = self.__expected_queue_length + 1
        print("Expected queue length:%s" % self.__expected_queue_length)
        if this_dev.email_list is None:
            recipients = []
        else:
            recipients = this_dev.email_list

        recipients.append(self.__config.email_name)
        self.__email_queue = self.__email_queue_manager.get_queue()
        if self.__email_queue is None:
            self.__email_queue = EmailQueue.construct_from_jdict({this_dev.device_tag: message})

        else:
            self.__email_queue.add_item(this_dev.device_tag, message)
            print("Current queue length:%s" % len(self.__email_queue.queue))
        while not self.__email_queue_manager.set_queue(self.__email_queue):
            continue

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

    def generate_email(self, device, byline_topic=None, field_name=None, field_type=None):
        template = None
        old_status = "inactive" if device.is_active else "active"
        now_status = "active" if device.is_active else "inactive"

        # Get templates
        if device.dm_status == "activity_change":
            template = "status_changed.txt"
        elif device.dm_status == "byline":
            template = "byline_inactive.txt"
        elif device.dm_status == "reboot":
            template = "uptime.txt"
        elif device.dm_status == "values":
            template = "values.txt"

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
        message = (message.replace("NEW_STATUS", now_status))
        message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))
        message = (message.replace("TOPIC_NAME", byline_topic if byline_topic else ""))
        message = (message.replace("TIME_ALLOWED", str(self.__config.unresponsive_minutes_allowed)))
        message = (message.replace("NOW_UPTIME", device.uptime if device.uptime else ""))
        message = (message.replace("FIELD_NAME", field_name if field_name else ""))
        message = (message.replace("FIELD_TYPE", field_type if field_type else ""))
        self.send_email_alert(device, message)

    def get_last_run_time(self):
        now = LocalizedDatetime.now()
        td = Timedelta(minutes=self.__RUN_FREQUENCY_MINUTES)
        res = now - td
        return res.as_json()

    def recreate_status_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            json_data[device.device_tag] = device.is_active
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_STATUS)

    def recreate_uptime_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            data = (device.as_uptime_json())
            json_data[data["dev-tag"]] = data["uptime"]
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)

    def recreate_pub_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            json_data[device.device_tag] = device.byline_status
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_BYLINES)

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
