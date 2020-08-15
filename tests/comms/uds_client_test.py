#!/usr/bin/env python3

"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from scs_core.comms.uds_client import UDSClient


# --------------------------------------------------------------------------------------------------------------------
# resources...

location = os.getcwd()
path = os.path.join(location, 'lambda-model.uds')

client = UDSClient(path)


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    client.connect()
    print(client)

    while True:
        client.request('hello')
        print('requested')

        message = client.wait_for_response()
        print(message)

        time.sleep(4)

except KeyboardInterrupt:
    print()

finally:
    client.disconnect()
    print('disconnected')
