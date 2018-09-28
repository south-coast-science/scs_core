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

message = '{"tag": "scs-bgx-122", "rec": "2018-04-05T10:57:49.178+00:00", "val": {"per": 10.0, "pm1": 4.4, ' \
          '"pm2p5": 6.6, "pm10": 11.1, "bins": {"0": 265, "1": 38, "2": 45, "3": 18, "4": 7, "5": 9, "6": 11, ' \
          '"7": 3, "8": 3, "9": 1, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0}, "mtf1": 19, "mtf3": 27, ' \
          '"mtf5": 29, "mtf7": 29}}'

start_time = time.time()

queue = MessageQueue(queue_size)
print(queue)

vm = psutil.virtual_memory()
print("vm: %s" % str(vm))

queue.start()
print("-")

print("queue: %s" % queue)
print("length: %s" % queue.length())
print("oldest: %s" % queue.oldest())
print("-")

for _ in range(queue_size):
    queue.enqueue(message)

print("queue: %s" % queue)
print("length: %s" % queue.length())
print("oldest: %s" % queue.oldest())

vm = psutil.virtual_memory()
print("vm: %s" % str(vm))

queue.stop()

elapsed_time = time.time() - start_time
time_per_message = elapsed_time / queue_size

print("elapsed_time: %0.1f (%0.3f per message)" % (elapsed_time, time_per_message))

print("-")
