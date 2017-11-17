"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
    "period": 604800,
    "last-reading": "5 seconds ago",
    "average-frequency": "9 seconds",
    "total": 49661,
    "contributors": [
      {
        "name": "South Coast Science - Dev",
        "id": "southcoastscience-dev",
        "gravatar-hash": "07f512e9fe64863039df0c0f1834cc25"
      }
    ]
    "last-location": {
      "lat": 50.819456,
      "lon": -0.128336
    }
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable

from scs_core.osio.data.topic_contributor import TopicContributor
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

class TopicStats(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        period = jdict.get('period')
        last_reading = jdict.get('last-reading')
        average_frequency = jdict.get('average-frequency')
        total = jdict.get('total')

        contributors_jdict = jdict.get('contributors')

        contributors = [TopicContributor.construct_from_jdict(contributor_jdict)
                        for contributor_jdict in contributors_jdict] if contributors_jdict else []

        last_location = Location.construct_from_jdict(jdict.get('last-location'))

        return TopicStats(period, last_reading, average_frequency, total, contributors, last_location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, period, last_reading, average_frequency, total, contributors, last_location):
        """
        Constructor
        """
        self.__period = period                          # int
        self.__last_reading = last_reading              # string
        self.__average_frequency = average_frequency    # string
        self.__total = total                            # int

        self.__contributors = contributors              # list of TopicContributor
        self.__last_location = last_location            # Location


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['period'] = self.period
        jdict['last-reading'] = self.last_reading
        jdict['average-frequency'] = self.average_frequency
        jdict['total'] = self.total

        jdict['contributors'] = self.contributors
        jdict['last-location'] = self.last_location

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def period(self):
        return self.__period


    @property
    def last_reading(self):
        return self.__last_reading


    @property
    def average_frequency(self):
        return self.__average_frequency


    @property
    def total(self):
        return self.__total


    @property
    def contributors(self):
        return self.__contributors


    @property
    def last_location(self):
        return self.__last_location


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        contributors = '[' + ', '.join(str(contributor) for contributor in self.contributors) + ']'

        return "TopicStats:{period:%s, last_reading:%s, average_frequency:%s, total:%s, contributors:%s, " \
               "last_location:%s}" % \
               (self.period, self.last_reading, self.average_frequency, self.total, contributors,
                self.last_location)
