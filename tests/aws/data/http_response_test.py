#!/usr/bin/env python3

"""
Created on 13 Jan 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse


# --------------------------------------------------------------------------------------------------------------------

response = HTTPResponse(HTTPStatus.CONFLICT, body="hello")
print(response)
print(response.as_http())
print(response.as_http()['body'])

response = HTTPResponse.construct_from_response_jdict(HTTPStatus.CONFLICT, json.loads(response.as_http()['body']))
print(response)

print("-")

response = HTTPResponse(HTTPStatus.OK)
print(response)
print(response.as_http())
print(response.as_http()['body'])

response = HTTPResponse.construct_from_response_jdict(HTTPStatus.OK, json.loads(response.as_http()['body']))
print(response)

