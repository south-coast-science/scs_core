"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50, "env": {"hmd": 66.0, "tmp": 11.0, "pA": 99.0}}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SensorBaseline(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return SensorBaseline(None, 0, None)

        if 'calibrated_on' in jdict:                            # TODO: deprecated
            date = Datum.date(jdict.get('calibrated_on'))
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = Datum.datetime(jdict.get('calibrated-on'))

        offset = jdict.get('offset')
        environment = BaselineEnvironment.construct_from_jdict(jdict.get('env'))

        return SensorBaseline(calibrated_on, offset, environment)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, offset, environment):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on            # LocalizedDatetime

        self.__offset = Datum.int(offset)               # int                       ppb
        self.__environment = environment                # BaselineEnvironment


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = None if self.calibrated_on is None else self.calibrated_on.as_iso8601(False)

        jdict['offset'] = self.offset
        jdict['env'] = self.environment

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def offset(self):
        return self.__offset


    @property
    def environment(self):
        return self.__environment


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorBaseline:{calibrated_on:%s, offset:%s, environment:%s}" % \
               (self.calibrated_on, self.offset, self.environment)


# --------------------------------------------------------------------------------------------------------------------

class BaselineEnvironment(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        humid = jdict.get('hmd')
        temp = jdict.get('tmp')
        press = jdict.get('pA')

        return BaselineEnvironment(humid, temp, press)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, humid, temp, press):
        """
        Constructor
        """
        self.__humid = Datum.float(humid, 1)            # float                 %
        self.__temp = Datum.float(temp, 1)              # float                 °C
        self.__press = Datum.float(press, 1)            # float                 kPa


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['hmd'] = self.humid
        jdict['tmp'] = self.temp
        jdict['pA'] = self.press

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def humid(self):
        return self.__humid


    @property
    def temp(self):
        return self.__temp


    @property
    def press(self):
        return self.__press


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BaselineEnvironment:{humid:%s, temp:%s, press:%s}" % (self.humid, self.temp, self.press)
