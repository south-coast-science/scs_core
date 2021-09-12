"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU is present, if any

example JSON:
{"model": "MobileV2", "batt-model": "PackV1", "ignore-threshold": true, "reporting-interval": 10,
"report-file": "/tmp/southcoastscience/psu_status_report.json"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(PersistentJSONable):
    """
    classdocs
    """

    __DEFAULT_REPORTING_INTERVAL = 10               # seconds

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
        report_file = jdict.get('report-file')

        return cls(psu_model, batt_model, ignore_threshold, reporting_interval, report_file)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu_model, batt_model, ignore_threshold, reporting_interval, report_file):
        """
        Constructor
        """
        super().__init__()

        self.__psu_model = psu_model                                        # string
        self.__batt_model = batt_model                                      # string
        self.__ignore_threshold = ignore_threshold                          # bool

        self.__reporting_interval = int(reporting_interval)                 # int
        self.__report_file = report_file                                    # string


    def __eq__(self, other):
        try:
            return self.psu_model == other.psu_model and \
                   self.batt_model == other.batt_model and \
                   self.ignore_threshold == other.ignore_threshold and \
                   self.reporting_interval == other.reporting_interval and \
                   self.report_file == other.report_file

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
    def report_file(self):
        return self.__report_file


    @property
    def reporting_interval(self):
        return self.__reporting_interval


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__psu_model
        jdict['batt-model'] = self.__batt_model
        jdict['ignore-threshold'] = self.__ignore_threshold

        jdict['reporting-interval'] = self.__reporting_interval
        jdict['report-file'] = self.__report_file

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf(core):{psu_model:%s, batt_model:%s, ignore_threshold:%s, reporting_interval:%s, " \
               "report_file:%s}" % \
               (self.psu_model, self.batt_model, self.ignore_threshold, self.reporting_interval,
                self.report_file)
