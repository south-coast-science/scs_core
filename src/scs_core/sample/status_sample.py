"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-06T11:13:07Z", "tag": "scs-be2-3", "ver": 1.00, "val": {"tz": {"name": "Europe/London",
"utc-offset": "+01:00"}, "gps": {"pos": [null, null], "elv": null, "qual": 0},
"sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-status": {"interval": 60.0, "tally": 1}}, "tmp": {"brd": 29.4}, "up": {"period": "00-00:22:00", "users": 3,
"load": {"av1": 0.02, "av5": 0.34, "av15": 0.67}}, "sig": {"quality": null, "recent": null}}}
"""

from collections import OrderedDict

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.data.datetime import LocalizedDatetime

from scs_core.location.timezone import Timezone

from scs_core.position.gps_datum import GPSDatum

from scs_core.sample.sample import Sample

from scs_core.sync.schedule import Schedule

from scs_core.sys.modem import Signal
from scs_core.sys.system_temp import SystemTemp
from scs_core.sys.uptime_datum import UptimeDatum


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    VERSION = 1.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = float(jdict.get('ver'))
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        val = jdict.get('val')

        # StatusSample...
        airnow = AirNowSiteConf.construct_from_jdict(val.get('airnow'))
        timezone = Timezone.construct_from_jdict(val.get('tz'))
        position = GPSDatum.construct_from_jdict(val.get('gps'))
        temperature = SystemTemp.construct_from_jdict(val.get('tmp'))
        schedule = Schedule.construct_from_jdict(val.get('sch'))
        uptime = UptimeDatum.construct_from_jdict(val.get('up'))
        modem_signal = Signal.construct_from_jdict(val.get('sig'))

        # PSUReport classes are not available to the scs_core package

        return cls(tag, rec, airnow, timezone, position, temperature, schedule, uptime, val.get('psu'), modem_signal,
                   version=version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, airnow, timezone, position, temperature, schedule, uptime, psu_report, modem_signal,
                 version=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, rec, version)

        self.__airnow = airnow                                      # AirNowSiteConf
        self.__timezone = timezone                                  # Timezone
        self.__position = position                                  # GPSDatum
        self.__temperature = temperature                            # HostStatus
        self.__schedule = schedule                                  # Schedule
        self.__uptime = uptime                                      # UptimeDatum
        self.__psu_report = psu_report                              # PSUReport
        self.__modem_signal = modem_signal                          # Signal


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

        if self.modem_signal is not None:
            jdict['sig'] = self.modem_signal.as_json()

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


    @property
    def modem_signal(self):
        return self.__modem_signal


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatusSample:{tag:%s, rec:%s, airnow:%s, timezone:%s, position:%s, " \
               "temperature:%s, schedule:%s, uptime:%s, psu_report:%s, modem_signal:%s}" % \
            (self.tag, self.rec, self.airnow, self.timezone, self.position,
             self.temperature, self.schedule, self.uptime, self.psu_report, self.modem_signal)
