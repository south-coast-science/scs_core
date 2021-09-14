"""
Created on 23 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str

from scs_core.estate.configuration import Configuration

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # Sample...
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        tag = jdict.get('tag')

        try:
            val_jdict = json.loads(jdict.get('val'))
        except TypeError:
            val_jdict = jdict.get('val')

        configuration = Configuration.construct_from_jdict(val_jdict)

        return cls(tag, rec, configuration)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, configuration):
        """
        Constructor
        """
        super().__init__(tag, rec)

        self.__configuration = configuration                # Configuration


    def __eq__(self, other):
        try:
            return self.tag == other.tag and self.configuration == other.configuration

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        if self.tag < other.tag:
            return True

        if self.tag > other.tag:
            return False

        if self.rec < other.rec:
            return True

        return False


    def diff(self, other):
        return ConfigurationSample(self.tag, self.rec, self.configuration.diff(other.configuration))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = None if self.rec is None else self.rec.as_iso8601()
        jdict['val'] = self.values

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        return self.configuration.as_json()


    @property
    def configuration(self):
        return self.__configuration


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationSample:{tag:%s, rec:%s, configuration:%s}" % (self.tag, self.rec, self.configuration)


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationSampleHistory(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, latest_only=False, items=None):
        """
        Constructor
        """
        self.__latest_only = latest_only                            # bool
        self.__items = {} if items is None else items               # dict of tag: list of ConfigurationSample


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, sample: ConfigurationSample):
        if sample.tag not in self.__items:
            self.__items[sample.tag] = []
            self.__items[sample.tag].append(sample)
            return

        if not self.__items[sample.tag] or not self.__latest_only:
            if sample not in self.__items[sample.tag]:            # we might not be reading all the fields in the DB!
                self.__items[sample.tag].append(sample)
            return

        for item in self.__items[sample.tag]:
            if sample.rec > item.rec:
                self.__items[sample.tag] = (sample, )
                return


    # ----------------------------------------------------------------------------------------------------------------

    def diffs(self):
        diff_history = ConfigurationSampleHistory()

        for tag in self.tags():
            prev = None
            for item in self.items_for_tag(tag):
                diff_history.insert(item if prev is None else item.diff(prev))
                prev = item

        return diff_history


    def tags(self):
        return set(self.__items.keys())


    def items_for_tag(self, tag):
        if tag not in self.__items:
            return None

        return self.__items[tag]


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        items = []

        for tag in self.tags():
            items += self.items_for_tag(tag)

        return items


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationSampleHistory:{latest_only:%s, items:%s}" % \
               (self.__latest_only, Str.collection(self.__items))


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationReport(ConfigurationSample):
    """
    classdocs
    """

    @classmethod
    def construct(cls, sample: ConfigurationSample, report: LocalizedDatetime):
        return cls(sample.tag, sample.rec, sample.configuration, report)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, configuration, report):
        """
        Constructor
        """
        super().__init__(tag, rec, configuration)

        self.__report = report                          # LocalizedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = {'report': self.report.as_iso8601(), 'update': self.rec.as_iso8601()}
        jdict['val'] = self.values

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def report(self):
        return self.__report


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationReport:{tag:%s, rec:%s, configuration:%s, report:%s}" % \
               (self.tag, self.rec, self.configuration, self.report)


