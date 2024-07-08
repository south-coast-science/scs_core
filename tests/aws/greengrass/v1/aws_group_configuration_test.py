#!/usr/bin/env python3

"""
Created on 11 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.greengrass.v1.aws_group_configuration import AWSGroupConfiguration


# --------------------------------------------------------------------------------------------------------------------

templates = AWSGroupConfiguration.templates()
print(templates)

# old style...

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z", "unix-group": 987, "ml": true}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z", "unix-group": 987, "ml": false}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

# new style...

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z", "unix-group": 987, "ml": "oE1"}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

