"""
Created on 6 Dec 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
ricardo/rural/device/praxis-000431/status
ricardo/rural/loc/1/particulates
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class TopicPath(JSONable):
    """
    classdocs
   """

    @classmethod
    def is_valid(cls, path_pieces):
        if len(path_pieces) != 5:
            return False

        for piece in path_pieces:
            if len(piece) < 1 or piece.startswith('-') or piece.endswith('-'):
                return False

        if len(path_pieces[0]) < 2:
            return False

        if path_pieces[2] != 'loc' and path_pieces[2] != 'device':
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, rec, path):
        path_pieces = path.strip('/').split('/')

        if not cls.is_valid(path_pieces):
            raise ValueError(path)

        return cls(rec, path_pieces)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        path_pieces = jdict.get('path').split('/')

        return cls(rec, path_pieces)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, path_pieces):
        """
        Constructor
        """
        self.__rec = rec                                        # LocalizedDatetime
        self.__path_pieces = path_pieces                        # array of string


    def __lt__(self, other):
        if self.__rec < other.rec:
            return True

        if self.__rec > other.rec:
            return False

        return self.path() < other.path()


    # ----------------------------------------------------------------------------------------------------------------
    # path type...

    def is_device_topic(self):
        return self.__path_pieces[2] == 'device'


    def is_environment_topic(self):
        return self.__path_pieces[2] == 'loc'


    # ----------------------------------------------------------------------------------------------------------------
    # path fields...

    def organisation(self):
        return self.__path_pieces[0]


    def project(self):
        return self.__path_pieces[1]


    def device(self):
        if not self.is_device_topic():
            raise ValueError(self.path())

        return self.__path_pieces[3]


    def location(self):
        if not self.is_environment_topic():
            raise ValueError(self.path())

        return self.__path_pieces[3]


    def phenomenon(self):
        return self.__path_pieces[-1]


    # ----------------------------------------------------------------------------------------------------------------
    # path structure...

    def root(self):
        return self.__path_pieces[0] + '/'


    def generic(self):
        return '/'.join(self.__path_pieces[:-1]) + '/'


    def path(self):
        return '/'.join(self.__path_pieces)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def path_pieces(self):
        return self.__path_pieces


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec
        jdict['path'] = self.path()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicPath:{rec:%s, path:%s}" % (self.rec, self.path())


# --------------------------------------------------------------------------------------------------------------------

class DeviceTopicGroup(object):
    """
    classdocs
   """

    @classmethod
    def construct(cls, bylines_for_device):
        device_topics = {}
        environment_topics = {}

        for byline in bylines_for_device:
            topic = TopicPath.construct(byline.rec, byline.topic)

            if topic.is_environment_topic():
                environment_topics[topic.generic()] = topic

            elif topic.is_device_topic():
                device_topics[topic.generic()] = topic

        return cls(sorted(device_topics.values()), sorted(environment_topics.values()))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_topics, environment_topics):
        """
        Constructor
        """
        self.__device_topics = device_topics                            # list of TopicPath
        self.__environment_topics = environment_topics                  # list of TopicPath


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_topics(self):
        return self.__device_topics


    @property
    def environment_topics(self):
        return self.__environment_topics


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceTopicGroup:{device_topics:%s, environment_topics:%s}" % \
               (Str.collection(self.device_topics), Str.collection(self.environment_topics))


# --------------------------------------------------------------------------------------------------------------------

class TopicGroup(object):
    """
    classdocs
   """

    @classmethod
    def construct_from_group(cls, topic_byline_group):
        device_topic_groups = {}

        for device in topic_byline_group.devices:
            device_topic_groups[device] = DeviceTopicGroup.construct(topic_byline_group.bylines_for_device(device))

        return cls(device_topic_groups)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_topic_groups):
        """
        Constructor
        """
        self.__device_topic_groups = device_topic_groups            # dict of string (device_tag): DeviceTopicGroup


    # ----------------------------------------------------------------------------------------------------------------

    def device_topic_group(self, device):
        return self.__device_topic_groups[device]                   # may raise KeyError


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_topic_groups(self):
        return self.__device_topic_groups


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicGroup:{device_topic_groups:%s}" % Str.collection(self.device_topic_groups)
