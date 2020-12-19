"""
Created on 18 Dec 2020

@author: Jade Page (Jade.Page@southcoastscience.com)

Based on
https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
https://gist.github.com/dbyr/8c9c04c63ac78da7eef57a7a3fc4ccc0

Uses the event to pull chunks of data from DynamoDB, without using the BOTO3 lib. So it's faster.
For this non-lambda'd version you must provide the key of a USER, not a ROLE.
They must have read permission for dynamo. Note that this code is just an example of pulling data out, beyond
counting how many lines it gets the data is not used.
"""
import datetime
import hashlib
import hmac
import json
import sys
import requests

from typing import *

from timeit import default_timer as timer


def lambda_handler(event, _context):
    topic = event.get("topic")
    time_start = event.get("start")
    time_end = event.get("end")

    do_query(topic, time_start, time_end)


def do_query(topic, start, end):
    t_start = timer()
    endpoint = "https://dynamodb.us-west-2.amazonaws.com/"
    lek = None
    lines = 0
    should_continue = True
    session = requests.session()

    aws_access_key = ""
    aws_secret_key = ""

    params = create_body(topic, start, end, lek)
    response = session.post(
        endpoint,
        data=params,
        headers=create_headers(
            access_key=aws_access_key,
            secret_key=aws_secret_key,
            request_parameters=params
        )
    )

    data = response.json()
    try:
        lek = data["LastEvaluatedKey"]
    except KeyError:
        should_continue = False

    lines = lines + len(data["Items"])

    while should_continue:
        params = create_body(topic, start, end, lek)
        response = session.post(
            endpoint,
            data=params,
            headers=create_headers(
                access_key=aws_access_key,
                secret_key=aws_secret_key,
                request_parameters=params
            )
        )

        data = response.json()
        try:
            lek = data["LastEvaluatedKey"]
        except KeyError:
            should_continue = False

        lines = lines + len(data["Items"])

    t_end = timer()
    print("Time:")
    print(t_end - t_start)
    print("Lines:")
    print(lines)


def create_body(topic, start, end, lek=None):
    params_dict = {
        "TableName": "messages",
        "KeyConditionExpression": "topic = :topic_name AND rec_at BETWEEN :start_time AND :end_time",
        "ExpressionAttributeValues": {
            ":topic_name": {"S": "%s" % topic},
            ":start_time": {"S": "%s" % start},
            ":end_time": {"S": "%s" % end},
        }
    }

    if lek:
        params_dict["ExclusiveStartKey"] = lek

    request_parameters = json.dumps(params_dict)
    return request_parameters


def create_headers(access_key, secret_key, request_parameters):
    region = "us-west-2"
    if access_key is None or secret_key is None:
        print("No access key is available.")
        sys.exit()

    service = "dynamodb"
    host = f"dynamodb.{region}.amazonaws.com"
    content_type = "application/x-amz-json-1.0"
    amz_target = "DynamoDB_20120810.Query"
    method = "POST"

    # Create a date for headers and the credential string
    t = datetime.datetime.utcnow()
    amz_date = t.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = t.strftime("%Y%m%d")

    canonical_uri = "/"
    canonical_querystring = ""
    canonical_headers = f"content-type:{content_type}\nhost:{host}\nx-amz-date:{amz_date}\nx-amz-target:{amz_target}\n"

    signed_headers = "content-type;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(request_parameters.encode("utf-8")).hexdigest()
    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}" \
                        f"\n{payload_hash}"

    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    request_digest = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{request_digest}"

    signing_key = get_singature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    authorization_header = f"{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, " \
                           f"Signature={signature} "

    headers = {
        "Content-Type": content_type,
        "X-Amz-Date": amz_date,
        "X-Amz-Target": amz_target,
        "Authorization": authorization_header,
    }
    return headers


def get_singature_key(key, date_stamp, region_name, service_name):
    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, "aws4_request")
    return k_signing


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def deserialize(value: Dict[str, Any], numeric_type: Callable[[str], Any]) -> Any:
    simple_types = frozenset({"BOOL", "S", "B"})
    simple_set_types = frozenset({"SS", "BS"})
    null_type = "NULL"

    if not value:
        raise TypeError(
            "Value error."
        )
    tag, val = next(iter(value.items()))
    if tag in simple_types:
        return val
    if tag == null_type:
        return None
    if tag == "N":
        return numeric_type(val)
    if tag in simple_set_types:
        return set(val)
    if tag == "NS":
        return {numeric_type(v) for v in val}
    if tag == "L":
        return [deserialize(v, numeric_type) for v in val]
    if tag == "M":
        return {k: deserialize(v, numeric_type) for k, v in val.items()}
    raise TypeError(f"Dynamodb type {tag} is not supported")


event = {
    "start": "2020-01-01T12:15:36Z",
    "end": "2020-07-11T12:15:36Z",
    "topic": "south-coast-science-demo/brighton/loc/1/climate"
}
lambda_handler(event, None)
