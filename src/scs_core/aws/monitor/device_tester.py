"""
Created on 08 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


class DeviceTester(object):
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, scs_device, config, host):
        """
        Constructor
        """
        self.__scs_device = scs_device
        self.__config = config
        self.__host = host

    # ----------------------------------------------------------------------------------------------------------------

    def is_inactive(self):
        latest_pub = self.__scs_device.latest_pub

        if latest_pub is None:
            return True

        now = LocalizedDatetime.now()
        delta = now - latest_pub

        return delta.minutes > self.__config.unresponsive_minutes_allowed

    def is_byline_inactive(self, byline):
        latest_pub = byline.pub
        if latest_pub is None:
            return True
        else:
            now = LocalizedDatetime.now()
            delta = now - latest_pub
            return delta.minutes > self.__config.unresponsive_minutes_allowed

    def has_status_changed(self, s3_device_status_list):
        is_active = not self.is_inactive()
        old_device_status_list = json.loads(s3_device_status_list)
        was_active = old_device_status_list[self.__scs_device.device_tag]
        if bool(is_active) == bool(was_active):
            return False
        else:
            return True

    def is_publishing_on_all_channels(self):
        device_bylines = self.__scs_device.bylines
        for byline in device_bylines:
            if self.is_byline_inactive(byline):
                return True, byline
            return False, None

    def check_values(self):
        # TODO check necessary values for nulls
        device_bylines = self.__scs_device.bylines
        for byline in device_bylines:
            if "gases" in byline.topic:
                message = byline.message
                if message is None:
                    return False

                json_message = json.loads(message)
                values = json_message.get("val")

                no2 = values.get("NO2")
                for key, value in no2.items():
                    if value is None:
                        return False, key, "NO2"

                ox = values.get("Ox")
                for key, value in ox.items():
                    if value is None:
                        return False, key, "Ox"

                co = values.get("CO")
                for key, value in co.items():
                    if value is None:
                        return False, key, "CO"

                sht = values.get("sht")
                for key, value in sht.items():
                    if value is None:
                        return False, key, "sht"

                so2 = values.get("SO2")
                for key, value in so2.items():
                    if value is None:
                        return False, key, "SO2"

            if "particulates" in byline.topic:
                message = byline.message
                if message is None:
                    return False

                json_message = json.loads(message)
                values = json_message.get("val")
                for key, value in values.items():
                    if value is None:
                        return False, key, "Particulates"

            return True, None, None


    def was_rebooted(self, s3_device_uptime_list):
        device_bylines = self.__scs_device.bylines

        old_device_uptime_list = json.loads(s3_device_uptime_list)
        old_period = old_device_uptime_list[self.__scs_device.device_tag]
        for byline in device_bylines:
            if "status" in byline.topic:
                message = byline.message
                if message is None:
                    return False
                json_message = json.loads(message)
                period = Timedelta().construct_from_jdict(json_message["val"]["up"]["period"])
                if old_period is not None:
                    delta_old_period = Timedelta().construct_from_jdict(old_period)
                    if period < delta_old_period:
                        # device has been reset
                        self.__scs_device.uptime = period.as_json()
                        return True
                    else:
                        # device has not been reset
                        self.__scs_device.uptime = period.as_json()
                        return False
                else:
                    return False

    # ----------------------------------------------------------------------------------------------------------------
