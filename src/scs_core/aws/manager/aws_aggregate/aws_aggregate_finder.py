"""
Created on 12 Mar 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Test client for live.southcoastscience.com aggregate finder
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import AWSEndpoint
from scs_core.aws.manager.topic_history.topic_history_intercourse import TopicHistoryRequest, TopicHistoryResponse

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(AWSEndpoint):
    @classmethod
    def configuration(cls):
        # return cls('topicMessages',
        #            'https://tkt93sk72l.execute-api.us-west-2.amazonaws.com/default/AWSAggregateTest')

        return cls('topicMessages',
                   'https://xef6bspqs5.execute-api.us-west-2.amazonaws.com/default/AWSAggregate')


# --------------------------------------------------------------------------------------------------------------------

class AWSAggregateFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topic(self, topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                       min_max, exclude_remainder, fetch_last_written_before, backoff_limit):

        request = TopicHistoryRequest(topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                                      min_max, exclude_remainder, fetch_last_written_before, backoff_limit)
        self._logger.debug(request)

        for item in self.__get_blocks(Endpoint.url(), TopicHistoryResponse, params=request.params()):
            yield item


    # ----------------------------------------------------------------------------------------------------------------

    def __get_blocks(self, url, block_class, params=None, payload=None):
        while True:
            response = requests.get(url, headers=self._auth_headers(), params=params, data=JSONify.dumps(payload))
            self._check_response(response)

            # self._logger.debug("response: %s" % response.json())

            # messages...
            block = block_class.construct_from_jdict(response.json())
            # self._logger.debug("block: %s" % block)

            for item in block.items:
                yield item

            # next request...
            if block.next_request is None:
                break

            params = block.next_params(params)
