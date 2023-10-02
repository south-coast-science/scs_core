"""
Created on 26 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

This version of MessageManager for AWS lambda function with multipart response.

Equivalent to cURL:
curl "https://aws.southcoastscience.com/topicMessages?topic=unep/ethiopia/loc/1/climate
&startTime=2018-12-13T07:03:59.712Z&endTime=2018-12-13T15:10:59.712Z"

Test endpoint:
curl "https://hb7aqje541.execute-api.us-west-2.amazonaws.com/default/AWSAggregateTest?topic=unep/ethiopia/loc/1/climate
&startTime=2018-12-13T07:03:59.712Z&endTime=2018-12-13T15:10:59.712Z"
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.manager.topic_history.topic_history_intercourse import TopicHistoryRequest, TopicHistoryResponse


# --------------------------------------------------------------------------------------------------------------------

class TopicHistoryManager(APIClient):
    """
    classdocs AWSAggregateTest
    """

    __URL = "https://60rd4rxw81.execute-api.us-west-2.amazonaws.com/default/TopicHistory"

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
        self._logger.debug(request)

        for item in self._get_blocks(self.__URL, token, TopicHistoryResponse, params=request.params()):
            yield item
