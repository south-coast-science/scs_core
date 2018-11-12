#!/usr/bin/env python3

"""
Created on 28 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import psutil
import time

from scs_core.data.message_queue import MessageQueue


# --------------------------------------------------------------------------------------------------------------------

queue_size = 21000      # 14 messages per minute * 60 * 24

message = '{"tag": "scs-be2-2", "src": "N2", "rec": "2018-11-11T09:05:10.424+00:00", ' \
          '"val": {"per": 10.0, "pm1": 8.1, "pm2p5": 12.1, "pm10": 12.9, ' \
          '"bins": [142, 63, 48, 28, 10, 13, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], ' \
          '"mtf1": 42, "mtf3": 44, "mtf5": 46, "mtf7": 59}}'

start_time = time.time()

queue = MessageQueue(queue_size)
print(queue)

vm = psutil.virtual_memory()
print("vm: %s" % str(vm))

queue.start()
print("-")

print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

for _ in range(queue_size):
    queue.enqueue(message)

print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())

vm = psutil.virtual_memory()
print("vm: %s" % str(vm))

queue.stop()

elapsed_time = time.time() - start_time
time_per_message = elapsed_time / queue_size

print("elapsed_time: %0.1f (%0.3f per message)" % (elapsed_time, time_per_message))

print("-")
