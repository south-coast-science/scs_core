#!/usr/bin/env python3

"""
Created on 11 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import logging

from scs_core.aws.data.ingestion.duplicate_publication import DuplicatePublication
from scs_core.aws.data.ingestion.ingestible_message import IngestibleMessage

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------
# logging...

Logging.config('duplicate_message_test', level=logging.INFO)
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
print(message)
print("-")

duplicate = DuplicatePublication.construct_from_message(message)
print(duplicate)
print("-")

print(duplicate.as_dynamo_json())
print("-")

print(JSONify.dumps(duplicate))

