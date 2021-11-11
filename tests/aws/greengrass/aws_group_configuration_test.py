#!/usr/bin/env python3

"""
Created on 11 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration


# --------------------------------------------------------------------------------------------------------------------

confs = AWSGroupConfiguration.list()
print(confs)

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z","unix-group": 987, "ml": true}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z","unix-group": 987, "ml": false}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

jstr = '{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z","unix-group": 987, "ml": "oE"}'

conf = AWSGroupConfiguration.construct_from_jdict(json.loads(jstr))
print(conf)
print("-")

