"""
Created on 26 Nov 2020

@author: Jade Page (Jade.Page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceReport(JSONable):

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('device_tag')
        bylines = jdict.get('bylines')
        power = jdict.get('power')
        status = jdict.get('status')
        uptime = jdict.get('uptime')
        emails = jdict.get('emails')

        return cls(device_tag, bylines, power, status, uptime, emails)

    @classmethod
    def construct_from_monitor(cls, device_tag, byline_list, power_list, status_list, uptime_list, email_list):
        failures = 0
        bylines = None
        power = None
        status = None
        uptime = None
        emails = None

        for key, value in byline_list.items():
            if key == device_tag:
                bylines = value

        for key, value in power_list.items():
            if key == device_tag:
                power = value

        for key, value in status_list.items():
            if key == device_tag:
                status = value

        for key, value in uptime_list.items():
            if key == device_tag:
                uptime = value

        for key, value in email_list.items():
            if key == device_tag:
                emails = value

        if bylines is None:
            failures += 1
        if power is None:
            failures += 1
        if status is None:
            failures += 1
        if uptime is None:
            failures += 1

        if failures > 3:
            return None

        return cls(device_tag, bylines, power, status, uptime, emails)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, bylines, power, status, uptime, emails):
        """
        Constructor
        """
        self.__device_tag = device_tag
        self.__bylines = bylines

        self.__power = power
        self.__status = status

        self.__uptime = uptime
        self.__emails = emails

    def as_json(self):
        jdict = OrderedDict()

        jdict['device_tag'] = self.device_tag
        jdict['bylines'] = self.bylines

        jdict['power'] = self.power
        jdict['status'] = self.status

        jdict['uptime'] = self.uptime
        jdict['emails'] = self.emails

        return jdict

    @property
    def device_tag(self):
        return self.__device_tag

    @property
    def bylines(self):
        return self.__bylines

    @property
    def power(self):
        return self.__power

    @property
    def emails(self):
        return self.__emails

    @property
    def status(self):
        return self.__status

    @property
    def uptime(self):
        return self.__uptime


    def __str__(self, *args, **kwargs):
        return "DeviceReport:{device_tag:%s, bylines:%s, power:%s, status:%s, uptime:%s, emails:%s}" %  \
               (self.device_tag, self.bylines, self.power, self.status, self.uptime, self.emails)

