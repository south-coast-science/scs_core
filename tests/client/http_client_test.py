#!/usr/bin/env python3

"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import socket
import time

from scs_core.client.http_client import HTTPClient


# --------------------------------------------------------------------------------------------------------------------

host = "slowwly.robertomurray.co.uk"
print("host:%s" % host)

# headers = {"Accept": "application/json", "Authorization": "api-key 43308b72-ad41-4555-b075-b4245c1971db"}
# print("headers:%s" % headers)

path = "/delay/3000/url/https://github.com"
print("path:%s" % path)

# params = {
#     'topic': 'south-coast-science-demo/brighton/loc/1/gases',
#     'startTime': '2020-04-22T10:14:00Z',
#     'endTime': '2020-04-22T10:15:00Z'
# }
#
# print("params:%s" % params)

# --------------------------------------------------------------------------------------------------------------------

client = HTTPClient()
client.connect(host, secure=False, timeout=2)
print(client)

try:
    while True:
        try:
            data = client.get(path, {}, {})
            print(data)

        except socket.timeout:
            print("timeout")
            time.sleep(2)

            client.connect(host, secure=False, timeout=2)

finally:
    client.close()

