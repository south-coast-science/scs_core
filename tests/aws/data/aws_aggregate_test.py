"""
Created on 02 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
# ----------------------------------------------------------------------------------------------------------------
import logging

from scs_core.aws.data.aws_aggregate import AWSAggregator
from scs_core.aws.data.dynamo_messages import DynamoMessages

from scs_core.data.datetime import LocalizedDatetime


def lambda_handler(event, _context):
    __MAX_LINES = 150

    status_code = 200
    res = None
    next_url = None
    topic = None
    start = None
    end = None
    checkpoint = None
    min_max = None

    aws_access_key =  ""
    aws_secret_key =  ""
    session_token = None

    qsp = event

    logging.getLogger().setLevel(logging.DEBUG)

    if qsp is None:
        status_code = 400
    if qsp.get("end") is None:
        end = LocalizedDatetime.now()
    if qsp is not None:
        topic = qsp.get("topic")
        start = qsp.get("start")
        end = qsp.get("end")
        min_max = qsp.get("mix_max") if "min_max" in qsp else False
        checkpoint = qsp.get("checkpoint")

    if topic is None or start is None:
        status_code = 400

    if start > end:
        status_code = 400

    logging.debug("Start:{}End:{}Check:{}Topic:{}MM:{}".format(start, end, checkpoint, topic, min_max))

    if status_code == 200:
        # try:
        if checkpoint is not None:
            logging.debug('Checkpoint, use AWSAggregator')
            aggregate = AWSAggregator(topic, start, end, checkpoint, __MAX_LINES, min_max, aws_access_key,
                                      aws_secret_key, session_token)
            aggregate.setup()
            res, next_url = aggregate.run()
        else:
            logging.debug('No checkpoint, use DynamoMessages')
            aws_messages = DynamoMessages(topic, start, end, True, __MAX_LINES, aws_access_key, aws_secret_key,
                                          session_token)
            res, next_url = aws_messages.run()
        #
        # except Exception as ex:
        #     res = "%s: %s" % (ex.__class__.__name__, ex)
        #     status_code = 500

    print(res)
    print(next_url)


test_event = {
    "start": "2020-01-01T12:15:36Z",
    "end": "2020-01-11T12:15:36Z",
    "topic": "south-coast-science-demo/brighton/loc/1/climate",
    "checkpoint": "**:/15:00"
}

lambda_handler(test_event, None)
