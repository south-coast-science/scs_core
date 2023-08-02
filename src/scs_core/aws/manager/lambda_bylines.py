"""
Created on 20 Sep 2022

@author: Jade Page (jade.page@southcoastscience.com)

Helper class for the bylines lambda
"""

import json


# ----------------------------------------------------------------------------------------------------------------

class BylineExclusiveStartKey(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        device = qsp.get('device')
        topic = qsp.get('topic')

        return cls(device, topic)


    @classmethod
    def construct_from_jdict(cls, jdict):
        return cls.construct_from_qsp(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic):
        """
        Constructor
        """
        self.__device = device                                      # string
        self.__topic = topic                                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            'device': self.device,
            'topic': self.topic
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


# --------------------------------------------------------------------------------------------------------------------

class BylineRequest(object):
    """
    classdocs
    """
    TAG_FILTER = 'device'
    TOPIC_FILTER = 'topic'
    EXCLUSIVE_START_KEY = 'exclusiveStartKey'
    START_EXCLUDE = 'startExclude'
    END_EXCLUDE = 'endExclude'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        tag_filter = qsp.get(cls.TAG_FILTER)
        topic_filter = qsp.get(cls.TOPIC_FILTER)

        esk_json = qsp.get(cls.EXCLUSIVE_START_KEY)
        exclusive_start_key = BylineExclusiveStartKey.construct_from_qsp(json.loads(esk_json)) if esk_json else None

        start_exclude = qsp.get(cls.START_EXCLUDE)
        end_exclude = qsp.get(cls.END_EXCLUDE)

        return cls(tag_filter, topic_filter, start_exclude, end_exclude, exclusive_start_key=exclusive_start_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag_filter, topic_filter, start_exclude, end_exclude, exclusive_start_key=None):
        """
        Constructor
        """
        self.__tag_filter = tag_filter                              # string
        self.__topic_filter = topic_filter                          # string

        self.__start_exclude = start_exclude
        self.__end_exclude = end_exclude

        self.__exclusive_start_key = exclusive_start_key  # ExclusiveStartKey


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {}

        if self.tag_filter is not None:
            params[self.TAG_FILTER] = self.tag_filter

        if self.topic_filter is not None:
            params[self.TOPIC_FILTER] = self.__topic_filter

        if self.start_exclude is not None:
            params[self.START_EXCLUDE] = self.__start_exclude

        if self.end_exclude is not None:
            params[self.END_EXCLUDE] = self.__end_exclude

        if self.exclusive_start_key is not None:
            params[self.EXCLUSIVE_START_KEY] = json.dumps(self.exclusive_start_key.params())

        return params

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag_filter(self):
        return self.__tag_filter


    @property
    def topic_filter(self):
        return self.__topic_filter

    @property
    def start_exclude(self):
        return self.__start_exclude

    @property
    def end_exclude(self):
        return self.__end_exclude

    @property
    def exclusive_start_key(self):
        return self.__exclusive_start_key


    @exclusive_start_key.setter
    def exclusive_start_key(self, exclusive_start_key):
        self.__exclusive_start_key = exclusive_start_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationRequest:{tag_filter:%s, topic_filter:%s, start_exclude:%s, end_exclude:%s," \
               " exclusive_start_key:%s}" % \
               (self.tag_filter, self.topic_filter, self.start_exclude, self.end_exclude, self.exclusive_start_key)
