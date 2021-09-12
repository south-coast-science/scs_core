"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which GPS receiver is present, if any, plus sample interval, tally and verbosity

example JSON:
{"model": "PAM7Q", "sample-interval": 10, "tally": 1, "report-file": "/tmp/southcoastscience/gps_report.json",
"debug": false}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class GPSConf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_SAMPLE_INTERVAL =       10          # seconds
    DEFAULT_TALLY =                 60          # 10 minutes


    __FILENAME = "gps_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        model = jdict.get('model')

        sample_interval = jdict.get('sample-interval', cls.DEFAULT_SAMPLE_INTERVAL)
        tally = jdict.get('tally', cls.DEFAULT_TALLY)
        report_file = jdict.get('report-file')
        debug = jdict.get('debug', False)

        return cls(model, sample_interval, tally, report_file, debug)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_interval, tally, report_file, debug):
        """
        Constructor
        """
        super().__init__()

        self.__model = model                                        # string

        self.__sample_interval = int(sample_interval)               # int seconds
        self.__tally = int(tally)                                   # int count
        self.__report_file = report_file                            # string tmp file to store current GPS report
        self.__debug = bool(debug)                                  # bool


    def __eq__(self, other):
        try:
            return self.model == other.model and self.sample_interval == other.sample_interval and \
                   self.tally == other.tally and self.report_file == other.report_file and \
                   self.debug == other.debug

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def gps_monitor(self, interface, host):
        return None


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def gps(self, interface, host):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def sample_interval(self):
        return self.__sample_interval


    @property
    def tally(self):
        return self.__tally


    @property
    def report_file(self):
        return self.__report_file


    @property
    def debug(self):
        return self.__debug


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model

        jdict['sample-interval'] = self.sample_interval
        jdict['tally'] = self.tally
        jdict['report-file'] = self.report_file
        jdict['debug'] = self.debug

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSConf(core):{model:%s, sample_interval:%s, tally:%s, report_file:%s, debug:%s}" % \
               (self.model, self.sample_interval, self.tally, self.report_file, self.debug)
