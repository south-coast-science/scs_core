#!/usr/bin/env python3

"""
Created on 6 Dec 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.manager.byline.byline import TopicBylineGroup

from scs_core.data.topic_path import TopicPath, TopicGroup
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

rec = LocalizedDatetime.now()
path = 'acsoft/holding-pool/device/praxis-000752/status'

topic = TopicPath.construct(rec, path)
print(topic)
print('is_device_topic: %s' % topic.is_device_topic())
print('is_environment_topic: %s' % topic.is_environment_topic())
print('phenomenon: %s' % topic.phenomenon())
print('generic: %s' % topic.generic())
print('-')

path = 'acsoft/holding-pool/loc/3/particulates'

topic = TopicPath.construct(rec, path)
print(topic)
print('is_device_topic: %s' % topic.is_device_topic())
print('is_environment_topic: %s' % topic.is_environment_topic())
print('phenomenon: %s' % topic.phenomenon())
print('generic: %s' % topic.generic())
print('-')

bylines_jstr = '''
[
    {
        "device": "scs-bgx-401",
        "topic": "south-coast-science-demo/brighton/device/praxis-000401/control",
        "lastSeenTime": "2022-11-30T03:18:17Z",
        "last_write": "2022-11-30T03:18:17Z"
    },
    {
        "device": "scs-bgx-401",
        "topic": "south-coast-science-demo/brighton/device/praxis-000401/status",
        "lastSeenTime": "2022-11-30T13:02:57Z",
        "last_write": "2022-11-30T13:02:56Z"
    },
    {
        "device": "scs-bgx-401",
        "topic": "south-coast-science-demo/brighton/loc/1/climate",
        "lastSeenTime": "2022-11-30T13:02:51Z",
        "last_write": "2022-11-30T13:02:50Z"
    },
    {
        "device": "scs-bgx-401",
        "topic": "south-coast-science-demo/brighton/loc/1/gases",
        "lastSeenTime": "2022-11-30T13:03:33Z",
        "last_write": "2022-11-30T13:03:33Z"
    },
    {
        "device": "scs-bgx-401",
        "topic": "south-coast-science-demo/brighton/loc/1/particulates",
        "lastSeenTime": "2022-11-30T13:03:34Z",
        "last_write": "2022-11-30T13:03:28Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/heathrow/device/praxis-000431/control",
        "lastSeenTime": "2022-12-06T03:18:17Z",
        "last_write": "2022-12-06T03:18:16Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/heathrow/device/praxis-000431/status",
        "lastSeenTime": "2022-12-06T14:45:36Z",
        "last_write": "2022-12-06T14:45:36Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/heathrow/loc/4/climate",
        "lastSeenTime": "2022-12-06T14:45:31Z",
        "last_write": "2022-12-06T14:45:30Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/heathrow/loc/4/gases",
        "lastSeenTime": "2022-12-06T14:45:43Z",
        "last_write": "2022-12-06T14:45:43Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/heathrow/loc/4/particulates",
        "lastSeenTime": "2022-12-06T14:45:54Z",
        "last_write": "2022-12-06T14:45:48Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/rural/device/praxis-000431/control",
        "lastSeenTime": null,
        "last_write": "2019-01-17T10:44:19Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/rural/device/praxis-000431/status",
        "lastSeenTime": null,
        "last_write": "2019-01-29T12:33:25Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/rural/loc/1/climate",
        "lastSeenTime": null,
        "last_write": "2019-01-29T12:33:24Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/rural/loc/1/gases",
        "lastSeenTime": null,
        "last_write": "2019-01-29T12:34:05Z"
    },
    {
        "device": "scs-bgx-431",
        "topic": "ricardo/rural/loc/1/particulates",
        "lastSeenTime": null,
        "last_write": "2019-01-29T12:33:57Z"
    }
]
'''

topic_byline_group = TopicBylineGroup.construct_from_jdict(json.loads(bylines_jstr))
print(topic_byline_group)

print("devices: %s" % topic_byline_group.devices)
print("bylines: %s" % [str(byline) for byline in topic_byline_group.bylines_for_device('scs-bgx-431')])
print("-")

topic_group = TopicGroup.construct_from_group(topic_byline_group)
print(topic_group)
print("-")

device_topic_group = topic_group.device_topic_group('scs-bgx-431')
print(device_topic_group)

