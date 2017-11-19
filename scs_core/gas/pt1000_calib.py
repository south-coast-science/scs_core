"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"v20": 0.322802, "calibrated_on": "2016-10-11"}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Calib(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "pt1000_calib.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        if 'calibrated_on' in jdict:                            # TODO: deprecated
            date = Datum.date(jdict.get('calibrated_on'))
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = Datum.datetime(jdict.get('calibrated-on'))

        v20 = jdict.get('v20')

        return Pt1000Calib(calibrated_on, v20)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, v20):
        """
        Constructor
        """
        super().__init__()

        self.__calibrated_on = calibrated_on        # LocalizedDatetime
        self.__v20 = Datum.float(v20, 6)            # voltage at 20 ºC


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        if self.__calibrated_on is None:
            self.__calibrated_on = LocalizedDatetime.now()

        super().save(host)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = self.calibrated_on
        jdict['v20'] = self.v20

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def v20(self):
        return self.__v20


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Pt1000Calib:{calibrated_on:%s, v20:%s}" % (self.calibrated_on, self.v20)
