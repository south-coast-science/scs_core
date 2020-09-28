"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

# --------------------------------------------------------------------------------------------------------------------
import json

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.client.email_client import EmailHandler
from scs_core.aws.manager.byline_manager import BylineManager
from scs_core.client.http_client import HTTPClient
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
        self.__watched_device_list = None
        self.__unresponsive_device_list = PathDict()
        self.__api_auth = APIAuth.load(host)
        self.__email_author = "devicetest147147@gmail.com"
        self.__email_password = "Southern!"
        self.__number_unresponsive = 0

    # ----------------------------------------------------------------------------------------------------------------

    def get_watched_device_list(self):
        data = '[{"device_tag":"scs-bgx-417","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-ph1-33","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-bgx-565","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-bgx-530","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-bgx-430","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-ap1-300","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-bgx-533","device_email":"jade.page@southcoastscience.com"},' \
               '{"device_tag":"scs-bgx-511","device_email":"jade.page@southcoastscience.com"}] '
        # IRL get data from database or something
        self.__watched_device_list = json.loads(data)

    def get_unresponsive_devices_list(self):
        for index, device in enumerate(self.__watched_device_list):
            device_data = self.get_byline_data(device["device_tag"])
            latest_activity = self.get_latest_response(device_data)
            if self.is_unresponsive(latest_activity):
                this_dev = self.__watched_device_list[index]
                self.__unresponsive_device_list.append(str(self.__number_unresponsive), this_dev)
                self.__number_unresponsive += 1

    def send_email_alerts(self):
        email_handler = EmailHandler(465, "smtp.gmail.com", self.__email_author, self.__email_password)
        iterations = 0
        while iterations < self.__number_unresponsive:
            this_dev = self.__unresponsive_device_list.node(str(iterations))
            this_dev_id = this_dev.get("device_tag")
            recipient = this_dev.get("device_email")
            message = "Device with ID %s has been unresponsive for at least %s minutes." % (this_dev_id, self.__unresponsive_minutes_allowed)
            email_handler.send_email(self.__email_author, recipient, message)
            iterations += 1

    def get_byline_data(self, device_tag):
        manager = BylineManager(HTTPClient(True), self.__api_auth)
        res = manager.find_bylines_for_device(device_tag).as_json()
        return res

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
            latest = j_byline["latest-pub"]
            if latest is not None:
                if cur_latest is None:
                    cur_latest = latest
                else:
                    if latest > cur_latest:
                        cur_latest = latest
        return cur_latest

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "device_monitor:{unresponsive_minutes_allowed:%s, watched_device_list:%s, unresponsive_device_list:%s"\ 
               "api_auth:%s, email_author:%s, number_unresponsive:%s }" % \
               (self.__unresponsive_minutes_allowed, self.__watched_device_list, self.__unresponsive_device_list,
                self.__api_auth, self.__email_author, self.__number_unresponsive)
