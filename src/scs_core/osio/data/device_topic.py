"""
Created on 2 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
    {
      "client_id": "5926",
      "owner": "southcoastscience-dev",
      "topic": "/orgs/south-coast-science-dev/development/loc/3/gases",
      "date": "2017-03-19T08:00:18.414Z",
      "payload": {
        "encoding": "utf-8",
        "content-type": "application/json",
        "text": "{"tag": "scs-ap1-6", "rec": "2017-03-19T08:00:17.601+00:00", "val":
        {"NO2": {"weV": 0.286379, "aeV": 0.288317, "weC": -0.014025, "cnc": -76.2},
        "Ox": {"weV": 0.416506, "aeV": 0.407381, "weC": null, "cnc": null},
        "NO": {"weV": 0.296255, "aeV": 0.31138, "weC": -0.036358, "cnc": -98.5},
        "CO": {"weV": 0.33413, "aeV": 0.566696, "weC": 0.34805, "cnc": 1456.3},
        "pt1": {"v": 0.324005, "tmp": 23.3},
        "sht": {"hmd": 45.4, "tmp": 21.9}}}"
      },
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceTopic(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_message_jdict(cls, jdict):
        if not jdict:
            return None

        client_id = jdict.get('device')
        path = jdict.get('topic')
        earliest_publication = LocalizedDatetime.construct_from_jdict(jdict.get('date'))

        client_id = DeviceTopic(client_id, path, earliest_publication)

        return client_id


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        client_id = jdict.get('client-id')
        path = jdict.get('path')
        earliest_publication = LocalizedDatetime.construct_from_jdict(jdict.get('earliest-pub'))

        client_id = DeviceTopic(client_id, path, earliest_publication)

        return client_id


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client_id, path, earliest_publication):
        """
        Constructor
        """
        self.__client_id = client_id                            # string (int by convention)
        self.__path = path                                      # string
        self.__earliest_publication = earliest_publication      # LocalisedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['client-id'] = self.client_id
        jdict['path'] = self.path
        jdict['earliest-pub'] = self.earliest_publication

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def client_id(self):
        return self.__client_id


    @property
    def path(self):
        return self.__path


    @property
    def earliest_publication(self):
        return self.__earliest_publication


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceTopic:{client_id:%s, path:%s, earliest_publication:%s}" % \
               (self.client_id, self.path, self.earliest_publication)
