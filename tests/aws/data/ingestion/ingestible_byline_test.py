#!/usr/bin/env python3

"""
Created on 11 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import logging

from scs_core.aws.data.ingestion.ingestible_byline import IngestibleByline
from scs_core.aws.data.ingestion.ingestible_message import IngestibleMessage

from scs_core.data.timedelta import Timedelta

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------
# logging...

Logging.config('ingestible_byline_test', level=logging.INFO)
logger = Logging.getLogger()


# --------------------------------------------------------------------------------------------------------------------
# resources...

with open('publication.json') as f:
    jdict = json.load(f)

print(jdict)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# run...

message = IngestibleMessage.construct_from_publication_jdict(jdict)
message.set_ttl(Timedelta(days=1))

print(message)
print("-")

print(message.as_json())
print("-")

byline = IngestibleByline.construct_from_message(message)
print(byline)
print("-")

print(byline.as_dynamo_json())

