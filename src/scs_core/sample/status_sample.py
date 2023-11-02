"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2023-10-18T08:15:05Z", "tag": "scs-bgx-882", "ver": 2.0, "val": {"tz": {"name": "Europe/London",
"utc-offset": "+01:00"}, "gps": {"pos": [50.82305824, -0.12288824], "elv": 60.3, "qual": 2},
"sch": {"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"tmp": {"brd": 30.7}, "up": {"period": "00-19:33:00", "users": 0, "load": {"av1": 0.15, "av5": 0.1, "av15": 0.1}},
"psu": {"src": "Ov1", "standby": false, "in": true, "pwr-in": 11.6, "rst": "FF", "chgr": "TFFF", "batt-flt": false,
"host-3v3": 3.4, "prot-batt": 8.3}, "net": {"eth0": {"kind": "ethernet", "state": "connected",
"conn": "Ethernet eth0"}, "cdc-wdm0": {"kind": "gsm", "state": "unavailable"}},
"sig": {"quality": 0, "recent": false}}}
"""

from collections import OrderedDict

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.data.datetime import LocalizedDatetime

from scs_core.location.timezone import Timezone

from scs_core.position.gps_datum import GPSDatum

from scs_core.sample.sample import Sample

from scs_core.sync.schedule import Schedule

from scs_core.sys.modem import Signal
from scs_core.sys.network import Networks
from scs_core.sys.system_temp import SystemTemp
from scs_core.sys.uptime_datum import UptimeDatum


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    VERSION = 2.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
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
        networks = Networks.construct_from_jdict(jdict.get('net'))

        # PSUReport classes are not available to the scs_core package

        return cls(tag, rec, airnow, timezone, position, temperature, schedule, uptime, val.get('psu'),
                   networks, modem_signal, version=version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, airnow, timezone, position, temperature, schedule, uptime, psu_report,
                 networks, modem_signal, version=None):
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
        self.__networks = networks                                  # Networks
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
            jdict['airnow'] = self.airnow

        if self.timezone is not None:
            jdict['tz'] = self.timezone

        if self.position is not None:
            jdict['gps'] = self.position

        jdict['sch'] = self.schedule
        jdict['tmp'] = self.temperature
        jdict['up'] = self.uptime

        if self.psu_report is not None:
            jdict['psu'] = self.psu_report

        jdict['net'] = self.networks

        if self.modem_signal is not None:
            jdict['sig'] = self.modem_signal

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
    def networks(self):
        return self.__networks


    @property
    def modem_signal(self):
        return self.__modem_signal


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatusSample:{tag:%s, rec:%s, airnow:%s, timezone:%s, position:%s, " \
               "temperature:%s, schedule:%s, uptime:%s, psu_report:%s, networks:%s, modem_signal:%s}" % \
            (self.tag, self.rec, self.airnow, self.timezone, self.position,
             self.temperature, self.schedule, self.uptime, self.psu_report, self.networks, self.modem_signal)
