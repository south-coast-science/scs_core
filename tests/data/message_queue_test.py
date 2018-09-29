#!/usr/bin/env python3

"""
Created on 27 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.message_queue import MessageQueue


# --------------------------------------------------------------------------------------------------------------------

queue = MessageQueue(3)
print(queue)

queue.start()
print("-")

print("start...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

queue.enqueue("hello")
time.sleep(1)

time.sleep(1)

print("enqueue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.enqueue("how are you")
time.sleep(1)

print("enqueue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.enqueue("goodbye")
time.sleep(1)

print("enqueue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.enqueue("extra")
time.sleep(1)

print("enqueue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.dequeue()
time.sleep(1)

print("dequeue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.dequeue()
time.sleep(1)

print("dequeue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.dequeue()
time.sleep(1)

print("dequeue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.dequeue()
time.sleep(1)

print("dequeue...")
print("queue: %s" % queue)
print("length: %s" % queue.length())
print("next: %s" % queue.next())
print("-")

time.sleep(1)

queue.stop()
print("-")
