"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

# --------------------------------------------------------------------------------------------------------------------
import boto3

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.client.email_client import EmailHandler
from scs_core.aws.data.device_line import DeviceLine
from scs_core.aws.manager.byline_manager import BylineManager
from scs_core.aws.manager.s3_manager import S3Manager
from scs_core.data import datetime
from scs_core.data.path_dict import PathDict
from scs_core.data.datetime import LocalizedDatetime, DateParser


class DeviceMonitor(object):
    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, unresponsive_minutes_allowed, host):
        """
        Constructor
        """
        self.__unresponsive_minutes_allowed = unresponsive_minutes_allowed
        self.__watched_device_list = {}
        self.__changed_device_list = {}
        self.__email_list = PathDict()
        self.__api_auth = APIAuth.load(host)
        self.__email_author = "devicetest147147@gmail.com"
        self.__email_password = "Southern!"
        self.__number_changed = 0
        self.__bucket_name = "scs-device-monitor"
        self.__bucket_resource = "TEST_DATA.json"

    # ----------------------------------------------------------------------------------------------------------------

    def get_watched_device_list(self):
        aws_client = boto3.client('s3', region_name='us-west-2')
        aws_resource_client = boto3.resource('s3', region_name='us-west-2')
        bucket_manager = S3Manager(aws_client, aws_resource_client)
        data = bucket_manager.retrieve_from_bucket(self.__bucket_name, self.__bucket_resource)

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
                    this_dev.dm_status = "Status: Became inactive"
                    self.__changed_device_list[self.__number_changed] = this_dev
                    self.__number_changed += 1
                this_dev.status_active = False
            else:
                if not this_dev.status_active:
                    this_dev.dm_status = "Status: Became active"
                    self.__changed_device_list[self.__number_changed] = this_dev
                    self.__number_changed += 1
                this_dev.status_active = True

    def send_email_alerts(self):
        email_handler = EmailHandler(465, "smtp.gmail.com", self.__email_author, self.__email_password)
        iterations = 0
        while iterations < self.__number_changed - 1:
            this_dev = self.__changed_device_list[iterations]
            recipients = this_dev.email_list

            message = "Device with ID %s \n message \n %s" % (this_dev.device_tag, this_dev.dm_status)
            for recipient in recipients:
                email_handler.send_email(self.__email_author, recipient, message)
            iterations += 1

    def get_byline_data(self, device_tag):
        manager = BylineManager(self.__api_auth)
        res = manager.find_bylines_for_device(device_tag)
        return res.as_json()

    def is_unresponsive(self, latest_activity):
        parser = DateParser.construct('YYYY-MM-DD')
        if latest_activity is None:
            return True
        now = LocalizedDatetime.now().utc()
        cutoff_time = LocalizedDatetime.now().utc() - datetime.timedelta(minutes=self.__unresponsive_minutes_allowed)
        iso_cutoff = LocalizedDatetime.construct_from_date_time(parser, str(cutoff_time.date()),
                                                                (cutoff_time.time()).strftime("%H:%M:%S "))
        if iso_cutoff > now:
            return True
        else:
            return False
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



    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "device_monitor:{unresponsive_minutes_allowed:%s, watched_device_list:%s, unresponsive_device_list:%s " \
               "api_auth:%s, email_author:%s, number_unresponsive:%s }" % \
               (self.__unresponsive_minutes_allowed, self.__watched_device_list, self.__changed_device_list,
                self.__api_auth, self.__email_author, self.__number_changed)
