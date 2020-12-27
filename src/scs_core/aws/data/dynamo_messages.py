"""
Created on 21 Dec 2020

@author: Jade Page (Jade.Page@southcoastscience.com)
"""

import logging

from urllib.parse import urlencode

from scs_core.aws.manager.dynamo_message_manager import MessageManager

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class DynamoMessages(object):
    """
    classdocs
    """

    __REQUEST_PATH = "/topicMessages"
    __END_POINT = "aws.southcoastscience.com"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, start, end, max_lines, access_key, secret_access_key, session_token):
        """
        Constructor
        """
        self.__start = start
        self.__end = end
        self.__topic = topic
        self.__message_manager = None
        self.__max_lines = max_lines
        self.__message_manager = MessageManager(access_key, secret_access_key, session_token)


    # ----------------------------------------------------------------------------------------------------------------

    def next_url(self, time):
        next_params = {
            'topic': self.__topic,
            'startTime': LocalizedDatetime,
            'endTime': self.__end
        }
        query = urlencode(next_params)

        url = 'https://{}{}?{}'.format(self.__END_POINT, self.__REQUEST_PATH, query)

        return url


    def run(self):
        res = []
        output_count = 0
        logging.debug(("aws_messages: start: %s" % self.__start))
        logging.debug(("aws_messages: end: %s" % self.__end))
        logging.debug(("aws_messages: topic: %s" % self.__topic))
        logging.debug(("aws_messages: max_lines: %s" % self.__max_lines))

        for message in self.__message_manager.find_for_topic(self.__topic, self.__start, self.__end):
            if output_count < self.__max_lines:
                res.append(message)
                output_count += 1
            else:
                payload = message.get("payload")
                next_time = payload.get("rec")
                next_url = self.next_url(next_time)
                jstr = JSONify.dumps(res)
                return jstr, next_url

        return res, None
