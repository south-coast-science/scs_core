#!/usr/bin/env python3

"""
Created on 12 Mar 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import logging

from scs_core.aws.manager.aws_aggregate.aws_aggregate_finder import AWSAggregateFinder

from scs_core.data.datetime import LocalizedDatetime

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('aws_aggregate_finder_test', level=logging.DEBUG)
logger = Logging.getLogger()

topic = 'south-coast-science-production/reference/loc/531/climate'
start = LocalizedDatetime.construct_from_iso8601('2024-03-12T09:00:00Z')
end = LocalizedDatetime.construct_from_iso8601('2024-03-12T09:10:00Z')
path = None
fetch_last = True
checkpoint = None
include_wrapper = False
rec_only = False
min_max = False
exclude_remainder = False
fetch_last_written_before = False
backoff_limit = None

# --------------------------------------------------------------------------------------------------------------------

finder = AWSAggregateFinder()
logger.info(finder)


found = finder.find_for_topic(topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                              min_max, exclude_remainder, fetch_last_written_before, backoff_limit)

for item in found:
    print(item)
