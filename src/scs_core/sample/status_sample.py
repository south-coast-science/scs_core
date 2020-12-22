"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-ap1-6", "rec": "2019-03-09T12:05:10Z", "val":
{"airnow": {"site": "850MM123456789", "pocs": {"88102": 2, "88103": 3}},
"tz": {"name": "Europe/London", "utc-offset": "+00:00"},
"sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"tmp": {"brd": 30.2, "hst": 47.8},
"up": {"period": "00-18:30:00", "users": 2, "load": {"av1": 0.0, "av5": 0.0, "av15": 0.0}}}}
"""

from collections import OrderedDict

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf
from scs_core.data.datetime import LocalizedDatetime
from scs_core.location.timezone import Timezone
from scs_core.position.gps_datum import GPSDatum
from scs_core.sample.sample import Sample
from scs_core.sync.schedule import Schedule
from scs_core.sys.system_temp import SystemTemp
from scs_core.sys.uptime_datum import UptimeDatum


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        val = jdict.get('val')

        # StatusSample...
        airnow = AirNowSiteConf.construct_from_jdict(val.get('airnow'))
        timezone = Timezone.construct_from_jdict(val.get('tz'))
        position = GPSDatum.construct_from_jdict(val.get('gps'))
        temperature = SystemTemp.construct_from_jdict(val.get('tmp'))
        schedule = Schedule.construct_from_jdict(val.get('sch'))
        uptime = UptimeDatum.construct_from_jdict(val.get('up'))

        # PSUReport classes are not available to the scs_core package

        return cls(tag, rec, airnow, timezone, position, temperature, schedule, uptime, val.get('psu'))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, airnow, timezone, position, temperature, schedule, uptime, psu_report):
        """
        Constructor
        """
        super().__init__(tag, rec)

        self.__airnow = airnow                                      # AirNowSiteConf
        self.__timezone = timezone                                  # Timezone
        self.__position = position                                  # GPSDatum
        self.__temperature = temperature                            # HostStatus
        self.__schedule = schedule                                  # Schedule
        self.__uptime = uptime                                      # UptimeDatum
        self.__psu_report = psu_report                              # PSUReport


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_invalid_value(cls):
        # TODO: implement has_invalid_value
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        jdict = OrderedDict()

        if self.airnow is not None:
            jdict['airnow'] = self.airnow.as_json()

        if self.timezone is not None:
            jdict['tz'] = self.timezone.as_json()

        if self.position is not None:
            jdict['gps'] = self.position.as_json()

        jdict['sch'] = self.schedule.as_json()
        jdict['tmp'] = self.temperature.as_json()
        jdict['up'] = self.uptime.as_json()

        if self.psu_report is not None:
            jdict['psu'] = self.psu_report.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def airnow(self):
        return self.__airnow


    @property
    def timezone(self):
        return self.__timezone


    @property
    def position(self):
        return self.__position


    @property
    def temperature(self):
        return self.__temperature


    @property
    def schedule(self):
        return self.__schedule


    @property
    def uptime(self):
        return self.__uptime


    @property
    def psu_report(self):
        return self.__psu_report


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatusSample:{tag:%s, rec:%s, airnow:%s, timezone:%s, position:%s, " \
               "temperature:%s, schedule:%s, uptime:%s, psu_report:%s}" % \
            (self.tag, self.rec, self.airnow, self.timezone, self.position,
             self.temperature, self.schedule, self.uptime, self.psu_report)
