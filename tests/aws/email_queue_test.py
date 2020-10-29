"""
Created on 28 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import time

from scs_core.aws.monitor.email_queue import EmailQueue
from scs_core.aws.monitor.email_queue_manager import EmailQueueManager

eq = EmailQueue()
eqm = EmailQueueManager()
eqm.start()


print (eq.as_json())
i = 0
while True:
    eq.add_item(i, "Hello")
    eqm.set_queue(eq)
    i = i + 1
    print("Running")
    time.sleep(5)