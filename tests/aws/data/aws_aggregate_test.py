"""
Created on 01 Dec 2020

@author: Jade Page (Jade.Page@southcoastscience.com)
"""
import logging

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.data.aws_aggregate import AWSAggregator
from scs_core.aws.data.aws_messages import AWSMessages
from scs_core.data.datetime import LocalizedDatetime
from scs_host.sys.host import Host


def run_aggregate_test():
    __MAX_LINES = 150
    api_auth = APIAuth.load(Host)
    topic = "south-coast-science-test/aws/loc/1/climate"
    start = "2020-01-11T12:15:36Z"
    start = LocalizedDatetime.construct_from_iso8601(start)
    end = "2020-12-02T15:25:49.046Z"
    # end = LocalizedDatetime.construct_from_iso8601(end)
    min_max = True
    # end = LocalizedDatetime.now()
    checkpoint = "**:/15:00"

    aggregator = AWSAggregator(api_auth, topic, start, end, checkpoint, __MAX_LINES, min_max)
    aggregator.setup()
    res, next_url = aggregator.run()
    print(next_url)
    print(res)


def run_messages_test():
    __MAX_LINES = 150
    api_auth = APIAuth.load(Host)
    topic = "south-coast-science-test/aws/loc/1/climate"
    start = "2020-01-11T12:15:36Z"
    start = LocalizedDatetime.construct_from_iso8601(start)
    end = "2020-12-02T15:25:49.046Z"
    end = LocalizedDatetime.construct_from_iso8601(end)
    aws_messages = AWSMessages(api_auth, topic, start, end, __MAX_LINES)
    res, next_url = aws_messages.run()
    print(next_url)
    print(res)

logging.getLogger().setLevel(logging.DEBUG)
run_aggregate_test()
