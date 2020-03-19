"""
Created on 11 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The TimezoneConf subsystem enables the device user to set the reported timezone independently from the
system timezone. If no timezone_conf.json document is found, then the system "localzone" is used.

https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones

example JSON:
{"set-on": "2017-08-12T11:20:28.740+00:00", "name": "Europe/London"}
"""

from collections import OrderedDict

from tzlocal import get_localzone

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_core.location.timezone import Timezone


# --------------------------------------------------------------------------------------------------------------------

class TimezoneConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "timezone_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def system_name(cls):
        return get_localzone().zone


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return TimezoneConf(None, None)

        set_on = Datum.datetime(jdict.get('set-on'))
        name = jdict.get('name')

        return TimezoneConf(set_on, name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, set_on, name):
        """
        Constructor
        """
        self.__set_on = set_on                          # LocalizedDatetime
        self.__name = name                              # a Pytz timezone name or None


    # ----------------------------------------------------------------------------------------------------------------

    def timezone(self):
        return Timezone(self.reporting_name())


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        if self.__set_on is None:
            self.__set_on = LocalizedDatetime.now().utc()

        super().save(host)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['set-on'] = None if self.set_on is None else self.set_on.as_iso8601(False)
        jdict['name'] = self.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def uses_system_name(self):
        return self.name is None


    def reporting_name(self):
        return self.system_name() if self.uses_system_name() else self.name


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set_on(self):
        return self.__set_on


    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TimezoneConf:{set_on:%s, name:%s}" % (self.set_on, self.name)
