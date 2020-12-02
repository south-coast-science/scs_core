"""
Created on 01 Dec 2020

@author: Jade Page (Jade.Page@southcoastscience.com)
"""
from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.data.aws_aggregate import AWSAggregator
from scs_core.data.datetime import LocalizedDatetime
from scs_host.sys.host import Host


def run_aggregate_test():

    api_auth = APIAuth.load(Host)
    topic = "south-coast-science-test/aws/loc/1/climate"
    start = "2020-01-11T12:15:36Z"
    start = LocalizedDatetime.construct_from_iso8601(start)
    end = "2020-12-02T15:25:49.046Z"
    end = LocalizedDatetime.construct_from_iso8601(end)
    # end = LocalizedDatetime.now()
    checkpoint = "**:/15:00"

    aggy = AWSAggregator(api_auth, topic, start, end, checkpoint)
    aggy.setup()
    res, next_url = aggy.run()
    print(next_url)


run_aggregate_test()
