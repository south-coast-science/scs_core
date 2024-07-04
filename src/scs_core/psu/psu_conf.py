"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU is present, if any

example JSON:
{"model": "MobileV2", "batt-model": "PackV1", "ignore-threshold": true, "reporting-interval": 10}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(PersistentJSONable):
    """
    classdocs
    """

    __DEFAULT_REPORTING_INTERVAL = 10               # seconds

    __REPORT_FILENAME = "psu_status_report.json"

    @classmethod
    def report_file(cls, manager):
        return manager.tmp_file(cls.__REPORT_FILENAME)


    # ----------------------------------------------------------------------------------------------------------------


    __FILENAME = "psu_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        psu_model = jdict.get('model')
        batt_model = jdict.get('batt-model')
        ignore_threshold = jdict.get('ignore-threshold', False)

        reporting_interval = jdict.get('reporting-interval', cls.__DEFAULT_REPORTING_INTERVAL)

        return cls(psu_model, batt_model, ignore_threshold, reporting_interval)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu_model, batt_model, ignore_threshold, reporting_interval):
        """
        Constructor
        """
        super().__init__()

        self.__psu_model = psu_model                                        # string
        self.__batt_model = batt_model                                      # string
        self.__ignore_threshold = ignore_threshold                          # bool

        self.__reporting_interval = int(reporting_interval)                 # int


    def __eq__(self, other):
        try:
            return self.psu_model == other.psu_model and \
                   self.batt_model == other.batt_model and \
                   self.ignore_threshold == other.ignore_threshold and \
                   self.reporting_interval == other.reporting_interval

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def psu(self, host, interface_model):
        return None


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def psu_monitor(self, host, interface_model, ignore_standby):
        return None


    # noinspection PyMethodMayBeStatic
    def psu_class(self):
        return None


    # noinspection PyMethodMayBeStatic
    def psu_report_class(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def psu_model(self):
        return self.__psu_model


    @property
    def batt_model(self):
        return self.__batt_model


    @property
    def ignore_threshold(self):
        return self.__ignore_threshold


    @property
    def reporting_interval(self):
        return self.__reporting_interval


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['model'] = self.__psu_model
        jdict['batt-model'] = self.__batt_model
        jdict['ignore-threshold'] = self.__ignore_threshold

        jdict['reporting-interval'] = self.__reporting_interval

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf(core):{psu_model:%s, batt_model:%s, ignore_threshold:%s, reporting_interval:%s}" % \
               (self.psu_model, self.batt_model, self.ignore_threshold, self.reporting_interval)
