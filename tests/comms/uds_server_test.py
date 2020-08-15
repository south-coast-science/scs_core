#!/usr/bin/env python3

"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.comms.uds_server import UDSServer


# --------------------------------------------------------------------------------------------------------------------
# resources...

location = os.getcwd()
path = os.path.join(location, 'test.uds')

server = UDSServer(path)
print(server)


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    server.start()
    print(server)

    while True:
        message = server.wait_for_request()
        print('request: %s' % message)

        server.respond('response: %s' % message)

except KeyboardInterrupt:
    print()

finally:
    server.stop()
    print('stopped')
