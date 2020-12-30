"""
Created on 23 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
from scs_core.aws.client.api_auth import APIAuth

from scs_core.aws.client.rest_client import RESTClient

jdict = {
    "endpoint": "xef6bspqs5.execute-api.us-west-2.amazonaws.com/default/AWSAggregate",
    "api-key": "beepboop",
}

api_auth = APIAuth.construct_from_jdict(jdict)
payload = {
    "topic": "south-coast-science-test/aws/loc/1/climate",
    "start": "2020-01-01T12:15:36Z",
    "end": "2020-12-02T12:15:36Z",
    "checkpoint": "**:/15:00"
}
rest_client = RESTClient(api_auth)
rest_client.connect()
res = rest_client.get("/", payload)
print(res)
