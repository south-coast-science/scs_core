"""
Created on 23 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.estate.configuration import Configuration

from scs_core.data.datetime import LocalizedDatetime

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict, default=True):
        if not jdict:
            return None

        # Sample...
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        tag = jdict.get('tag')

        configuration = Configuration.construct_from_jdict(json.loads(jdict.get('value')))      # TODO: should be 'val'

        return cls(tag, rec, configuration)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, configuration):
        """
        Constructor
        """
        super().__init__(tag, rec)

        self.__configuration = configuration                # SHT31Datum


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        return self.configuration.as_json()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def configuration(self):
        return self.__configuration


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationSample:{tag:%s, rec:%s, configuration:%s}" % \
            (self.tag, self.rec, self.configuration)
