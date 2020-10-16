"""
Created on 08 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import ast

from scs_core.data.datetime import LocalizedDatetime


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
        old_device_status_list = ast.literal_eval(s3_device_status_list)
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

    # ----------------------------------------------------------------------------------------------------------------

