#!/usr/bin/env python3

"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import logging
import os
import sys

from scs_core.comms.uds_server import UDSServer


# --------------------------------------------------------------------------------------------------------------------
# resources...

# logging...
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# server...
location = os.getcwd()
path = os.path.join(location, 'lambda-model.uds')

server = UDSServer(path, logger=logger)
print(server)


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    server.start()
    print(server)

    for message in server.requests():
        print('request: %s' % message)

        server.respond(message)

except KeyboardInterrupt:
    print()

finally:
    server.stop()
