"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"calibrated-on": "2017-07-19T13:56:48.289+00:00", "v20": 0.002891}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Calib(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_V20 = 0.295                         # Volts at 20 °C

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "pt1000_calib.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        if 'calibrated_on' in jdict:                            # TODO: deprecated
            date = Datum.date(jdict.get('calibrated_on'))
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        v20 = jdict.get('v20')

        return Pt1000Calib(calibrated_on, v20)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, v20):
        """
        Constructor
        """
        super().__init__()

        self.__calibrated_on = calibrated_on        # LocalizedDatetime
        self.__v20 = Datum.float(v20, 6)            # voltage at 20 °C


    def __eq__(self, other):
        try:
            return self.calibrated_on == other.calibrated_on and self.v20 == other.v20

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host, encryption_key=None):
        if self.__calibrated_on is None:
            self.__calibrated_on = LocalizedDatetime.now().utc()

        super().save(host, encryption_key=encryption_key)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = self.calibrated_on.as_iso8601()
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
