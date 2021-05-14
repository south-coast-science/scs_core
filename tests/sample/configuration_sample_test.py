#!/usr/bin/env python3

"""
Created on 26 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.configuration import Configuration

from scs_core.sample.configuration_sample import ConfigurationSample, ConfigurationSampleHistory


# --------------------------------------------------------------------------------------------------------------------
# run...

history = ConfigurationSampleHistory()      # latest_only=True

rec = LocalizedDatetime.construct_from_iso8601('2021-04-26T11:00:13Z')
sample = ConfigurationSample('tag2', rec, Configuration.construct_from_jdict(json.loads('{"hostname": "host2"}')))
print(sample)

history.insert(sample)
print("-")

rec = LocalizedDatetime.construct_from_iso8601('2021-04-25T11:00:13Z')
sample = ConfigurationSample('tag2', rec, Configuration.construct_from_jdict(json.loads('{"hostname": "host2"}')))
print(sample)

history.insert(sample)
print("-")

rec = LocalizedDatetime.construct_from_iso8601('2021-04-26T11:00:13Z')
sample = ConfigurationSample('tag1', rec, Configuration.construct_from_jdict(json.loads('{"hostname": "host1"}')))
print(sample)

history.insert(sample)
print("-")

rec = LocalizedDatetime.construct_from_iso8601('2021-04-25T11:00:13Z')
sample = ConfigurationSample('tag1', rec, Configuration.construct_from_jdict(json.loads('{"hostname": "host1"}')))
print(sample)

history.insert(sample)
print("-")

print(JSONify.dumps(history.as_json(), indent=4))
print("-")

print("tags: %s" % history.tags())
print("-")

print("diffs...")
diffs = history.diffs()
print(JSONify.dumps(diffs.as_json(), indent=4))
print("-")
