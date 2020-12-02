"""
Created on 01 Dec 2020

@author: Jade Page (Jade.Page@southcoastscience.com)
"""
import json
import logging
from http.client import HTTPException
from urllib.parse import urlencode

from scs_core.aws.manager.lambda_message_manager import MessageManager

from scs_analysis.handler.aws_topic_history_reporter import AWSTopicHistoryReporter

from scs_core.data.datetime import LocalizedDatetime

from scs_core.data.path_dict import PathDict

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.manager.byline_manager import BylineManager

from scs_core.data.aggregate import Aggregate
from scs_core.data.checkpoint_generator import CheckpointGenerator


class AWSAggregator(object):
    __REQUEST_PATH = "/topicMessages"
    __MAX_LINES = 167
    __END_POINT = "aws.southcoastscience.com"

    def __init__(self, api_auth, topic, start, end, checkpoint):
        """
        Constructor
        """
        self.__api_auth = api_auth
        self.__start = start
        self.__end = end
        self.__topic = topic
        self.__checkpoint = checkpoint
        self.__generator = None
        self.__aggregate = None
        self.__rest_client = None
        self.__reporter = None
        self.__byline_manager = None
        self.__message_manager = None

        logging.getLogger().setLevel(logging.DEBUG)

    def setup(self):
        self.__generator = CheckpointGenerator.construct(self.__checkpoint)
        self.__aggregate = Aggregate(False, "rec", None)
        self.__rest_client = RESTClient(self.__api_auth)
        self.__reporter = AWSTopicHistoryReporter(False)
        self.__byline_manager = BylineManager(self.__api_auth)
        self.__message_manager = MessageManager(self.__api_auth, self.__reporter)

    def next_url(self, checkpoint):
        next_params = {
            'topic': self.__topic,
            'startTime': checkpoint.as_iso8601(False),
            'endTime': self.__end.as_iso8601(False),
        }
        query = urlencode(next_params)

        url = 'https://{}{}?{}'.format(self.__END_POINT, self.__REQUEST_PATH, query)

        return url

    def run(self):
        logging.debug(("aws_aggregate: start: %s" % self.__start))
        logging.debug(("aws_aggregate: end: %s" % self.__end))
        logging.debug(("aws_aggregate: topic: %s" % self.__topic))

        checkpoint = None
        prev_rec = None
        res = []

        try:
            document_count = 0
            output_count = 0
            processed_count = 0
            for message in self.__message_manager.find_for_topic(self.__topic, self.__start, self.__end, False):
                logging.debug("Got message")
                jstr = json.dumps(message.payload)
                datum = PathDict.construct_from_jstr(jstr)

                try:
                    rec_node = datum.node("rec")
                except KeyError:
                    continue

                document_count += 1
                logging.debug(("aws_aggregate: document_count: %s" % document_count))
                logging.debug(("aws_aggregate: document: %s" % datum))

                rec = LocalizedDatetime.construct_from_iso8601(rec_node)

                # set checkpoint...
                if checkpoint is None:
                    checkpoint = self.__generator.next_localised_datetime(rec)

                # report and reset...
                if rec > checkpoint:
                    self.__aggregate.print(checkpoint)
                    result = self.__aggregate.pass_back(checkpoint)
                    res.append(result)
                    output_count += 1
                    logging.debug(("aws_aggregate: output_count: %s" % output_count))

                    self.__aggregate.reset()
                    logging.debug("aws_aggregate: aggregate reset")

                    checkpoint = self.__generator.enclosing_localised_datetime(rec)

                # duplicate recs?...
                if rec == prev_rec:
                    logging.debug(("sample_aggregate: discarding duplicate: %s" % message.strip()))
                    continue

                # append sample...
                self.__aggregate.append(rec, datum)

                prev_rec = rec
                processed_count += 1

                if output_count >= self.__MAX_LINES:
                    return res, self.next_url(checkpoint)

        except HTTPException as ex:
            logging.error(("aws_topic_history: %s" % ex))
            exit(1)
