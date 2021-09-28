#!/usr/bin/env python3

"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.aws.manager.lambda_message_manager import MessageRequest


# --------------------------------------------------------------------------------------------------------------------

start = LocalizedDatetime.construct_from_iso8601('2020-01-01T00:00:00Z')
print(start)
print("-")


end = LocalizedDatetime.construct_from_iso8601('2020-01-01T01:00:00Z')
print(end)

request = MessageRequest('topic', start, end, None, False, 'auto', False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")


end = LocalizedDatetime.construct_from_iso8601('2020-01-02T00:00:00Z')
print(end)

request = MessageRequest('topic', start, end, None, False, 'auto', False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")


end = LocalizedDatetime.construct_from_iso8601('2020-01-08T00:00:00Z')
print(end)

request = MessageRequest('topic', start, end, None, False, 'auto', False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")


end = LocalizedDatetime.construct_from_iso8601('2020-02-01T00:00:00Z')
print(end)

request = MessageRequest('topic', start, end, None, False, 'auto', False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")


end = LocalizedDatetime.construct_from_iso8601('2021-01-01T00:00:00Z')
print(end)

request = MessageRequest('topic', start, end, None, False, 'auto', False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")

request = MessageRequest('topic', start, end, None, False, None, False, False, False, False, False, None)
print(request)

print('checkpoint: %s' % request.checkpoint)
print("-")

