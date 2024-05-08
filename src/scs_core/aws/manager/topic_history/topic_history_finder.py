"""
Created on 26 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

This version of MessageManager for AWS lambda function with multipart response.
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.manager.topic_history.topic_history_intercourse import TopicHistoryRequest, TopicHistoryResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('DataAPI/TopicHistory',
                   'https://60rd4rxw81.execute-api.us-west-2.amazonaws.com/default/TopicHistory')


# --------------------------------------------------------------------------------------------------------------------

class TopicHistoryFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_for_topic(self, token, topic, end, path, include_wrapper, rec_only, backoff_limit):
        documents = list(self.find_for_topic(token, topic, None, end, path, False, None, include_wrapper, rec_only,
                                             False, False, True, backoff_limit))
        if documents:
            return documents[0]

        return None


    def find_for_topic(self, token, topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                       min_max, exclude_remainder, fetch_last_written_before, backoff_limit):
        self._reporter.reset()

        request = TopicHistoryRequest(topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                                      min_max, exclude_remainder, fetch_last_written_before, backoff_limit)
        self._logger.info(request.params())

        for item in self._get_blocks(Endpoint.url(), token, TopicHistoryResponse, params=request.params()):
            yield item
