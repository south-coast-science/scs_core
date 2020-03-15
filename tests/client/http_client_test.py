#!/usr/bin/env python3

"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.client.http_client import HTTPClient


# --------------------------------------------------------------------------------------------------------------------

host = "pokemon.p3d.co.uk"
print("host:%s" % host)

headers = {"Accept": "application/json", "Authorization": "api-key 43308b72-ad41-4555-b075-b4245c1971db"}
print("headers:%s" % headers)

path = "/get"
print("path:%s" % path)

params = {'a': 1}
print("params:%s" % params)

'''
host = "api.opensensors.io"
print("host:%s" % host)

headers = {"Accept": "application/json", "Authorization": "api-key 43308b72-ad41-4555-b075-b4245c1971db"}
print("headers:%s" % headers)

path = "/v1/orgs/south-coast-science-dev/topics"
print("path:%s" % path)
'''


# --------------------------------------------------------------------------------------------------------------------

client = HTTPClient(False)
client.connect(host)
print(client)

try:
    data = client.get(path, params, headers)
    print(data)

except Exception as ex:
    raise ex

finally:
    client.close()

