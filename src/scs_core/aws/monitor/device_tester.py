"""
Created on 08 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


class DeviceTester(object):
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, scs_device, config):
        """
        Constructor
        """
        self.__scs_device = scs_device
        self.__config = config

    # ----------------------------------------------------------------------------------------------------------------

    def is_inactive(self):
        latest_pub = self.__scs_device.latest_pub

        if latest_pub is None:
            return True

        now = LocalizedDatetime.now()
        delta = now - latest_pub

        elapsed_minutes = delta.total_seconds() / 60

        return elapsed_minutes > self.__config.unresponsive_minutes_allowed

    def get_byline_activity(self):
        device_data = OrderedDict()
        byline_list = self.__scs_device.bylines
        for line in byline_list:
            active = self.is_byline_active(line)
            topic = line.topic
            device_data[topic] = active
        self.__scs_device.byline_status = device_data

    def is_byline_active(self, byline):
        byline_minutes_allowed = self.__config.unresponsive_minutes_allowed * 1.5
        latest_pub = byline.pub
        if latest_pub is None:
            return False
        else:
            now = LocalizedDatetime.now()
            delta = now - latest_pub
            elapsed_minutes = delta.total_seconds() / 60

            return elapsed_minutes < byline_minutes_allowed


    def has_status_changed(self, s3_device_status_list):
        is_active = self.__scs_device.is_active
        was_active = s3_device_status_list[self.__scs_device.device_tag]
        if bool(is_active) == bool(was_active):
            return False
        else:
            return True

    def has_byline_status_changed(self, s3_byline_status_list):
        device_bylines = self.__scs_device.bylines
        device_tag = self.__scs_device.device_tag
        if device_tag in s3_byline_status_list:
            old_byline_status_list = s3_byline_status_list[device_tag]
            if old_byline_status_list is None:
                return False, False, ""
            for line in device_bylines:
                active = self.is_byline_active(line)
                topic = line.topic
                for key, value in old_byline_status_list.items():
                    if key == topic:
                        if value is not active:
                            if value is True:
                                return False, True, topic
                            if value is False:
                                return True, True, topic

        return False, False, None

    def check_values(self):

        device_bylines = self.__scs_device.bylines
        for byline in device_bylines:
            if "gases" in byline.topic:
                message = byline.message
                if message is None:
                    return True, None, None

                json_message = json.loads(message)
                values = json_message.get("val")

                no2 = values.get("NO2")
                for key, value in no2.items():
                    if value is None:
                        return False, "gases", byline

                ox = values.get("Ox")
                for key, value in ox.items():
                    if value is None:
                        return False, "gases", byline

                co = values.get("CO")
                for key, value in co.items():
                    if value is None:
                        return False, "gases", byline

                sht = values.get("sht")
                for key, value in sht.items():
                    if value is None:
                        return False, "gases", byline

                so2 = values.get("SO2")
                for key, value in so2.items():
                    if value is None:
                        return False, "gases", byline

            if "particulates" in byline.topic:
                message = byline.message
                if message is None:
                    return False

                json_message = json.loads(message)
                values = json_message.get("val")
                for key, value in values.items():
                    if value is None:
                        return False, "particulates", byline

            return True, None, None


    def was_rebooted(self, s3_device_uptime_list):
        device_bylines = self.__scs_device.bylines

        old_period = s3_device_uptime_list[self.__scs_device.device_tag]
        for byline in device_bylines:
            if "status" in byline.topic:
                message = byline.message
                if message is not None:
                    json_message = json.loads(message)
                    period = Timedelta().construct_from_jdict(json_message["val"]["up"]["period"])
                    if old_period is not None:
                        delta_old_period = Timedelta().construct_from_jdict(old_period)
                        if period < delta_old_period:
                            # device has been reset
                            self.__scs_device.uptime = period.as_json()
                            self.__scs_device.old_uptime = delta_old_period.as_json()
                            return True
                        else:
                            # device has not been reset
                            self.__scs_device.uptime = period.as_json()
                            return False
                    else:
                        self.__scs_device.uptime = period.as_json()
                        return False
        return False

    # ----------------------------------------------------------------------------------------------------------------
