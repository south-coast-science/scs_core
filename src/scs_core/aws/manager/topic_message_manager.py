"""
Created on 10 Dec 2020
Author: Jade Page (jade.page@southcoastscience.com)

Like lambda_message_manager, but speaks directly to the lambda
"""

# --------------------------------------------------------------------------------------------------------------------
import json
from urllib.parse import urlparse, parse_qs

from scs_core.aws.manager.lambda_message_manager import MessageResponse


class MessageManager(object):
    """
    classdocs
    """
    __TOPIC = 'topic'
    __START = 'startTime'
    __END = 'endTime'
    __REC_ONLY = 'rec_only'

    def __init__(self, lambda_client):
        """
        Constructor
        """
        self.__lambda_client = lambda_client

    def find_for_topic(self, topic, start_date, end_date):

        event = {'topic': topic,
                 'startTime': start_date.utc().as_iso8601(True),
                 'endTime': end_date.utc().as_iso8601(True)}

        while True:
            # request...
            payload = json.dumps(event).encode('utf-8')
            response = self.__lambda_client.invoke(
                FunctionName="arn:aws:lambda:us-west-2:696437392763:function:topicMessages",
                InvocationType='RequestResponse',
                Payload=payload
            )

            res = response['Payload'].read()

            j_res = json.loads(res.decode('utf-8'))
            body = json.loads(j_res.get("body"))

            # messages...
            block = MessageResponse.construct_from_jdict(body)

            for item in block.items:
                yield item

            if block.next_url is None:
                break

            next_url = urlparse(block.next_url)
            next_params = parse_qs(next_url.query)

            event = {'topic': topic,
                     'startTime': next_params[self.__START][0],
                     'endTime': end_date.utc().as_iso8601(True)}


