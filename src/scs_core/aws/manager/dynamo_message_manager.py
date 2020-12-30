"""
Created on 21 Dec 2020
Author: Jade Page (jade.page@southcoastscience.com)

Like lambda_message_manager, but speaks directly to dynamo
"""

# --------------------------------------------------------------------------------------------------------------------
import datetime
import hashlib
import hmac
import json
import logging
import requests

from typing import *

from scs_core.aws.manager.manager_error import InvalidKeyError


class MessageManager(object):
    """
    classdocs
    """
    __TOPIC = 'topic'
    __START = 'startTime'
    __END = 'endTime'
    __REC_ONLY = 'rec_only'

    def __init__(self, access_key, secret_access_key, session_token):
        """
        Constructor
        """
        self.__access_key = access_key
        self.__secret_access_key = secret_access_key
        self.__session_token = session_token

    def find_for_topic(self, topic, start, end):
        logging.debug('Begin requests...')
        endpoint = "https://dynamodb.us-west-2.amazonaws.com/"
        lek = None
        session = requests.session()

        aws_access_key = self.__access_key
        aws_secret_key = self.__secret_access_key
        session_token = self.__session_token

        while True:
            params = create_body(topic, start, end, lek)
            response = session.post(
                endpoint,
                data=params,
                headers=create_headers(
                    access_key=aws_access_key,
                    secret_key=aws_secret_key,
                    request_parameters=params,
                    session_token=session_token,
                )
            )
            logging.debug('Ok:')
            logging.debug(response.ok)
            logging.debug('Reason:')
            logging.debug(response.reason)
            data = response.json()

            for item in data["Items"]:
                logging.debug('Yield item')
                yield {key: deserialize(value, float) for key, value in item.items()}

            try:
                lek = data["LastEvaluatedKey"]
            except KeyError:
                break

    def check_auth(self, api_key):
        logging.debug('Check auth...')
        endpoint = "https://dynamodb.us-west-2.amazonaws.com/"
        session = requests.session()

        params_dict = {
            "TableName": "accounts",
            "KeyConditionExpression": "apiKey = :hkey",
            "ExpressionAttributeValues": {
                ":hkey": {"S": "%s" % api_key},
            }
        }

        params = json.dumps(params_dict)

        response = session.post(
            endpoint,
            data=params,
            headers=create_headers(
                access_key=self.__access_key,
                secret_key=self.__secret_access_key,
                request_parameters=params,
                session_token=self.__session_token,
            )
        )

        logging.debug('Ok:')
        logging.debug(response.ok)
        logging.debug('Reason:')
        logging.debug(response.reason)
        data = response.json()

        if len(data["Items"]) < 1:
            return False


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


def create_headers(access_key, secret_key, request_parameters, session_token):
    region = "us-west-2"
    if access_key is None or secret_key is None:
        print("No access key is available.")
        raise InvalidKeyError()

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

    signing_key = get_signature_key(secret_key, date_stamp, region, service)
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
        "X-Amz-Security-Token": session_token,
    }
    print(headers)
    return headers


def get_signature_key(key, date_stamp, region_name, service_name):
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
            "Dynamo Value error."
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
    raise TypeError(
        "Dynamo Value error."
    )


def get_auth_key(self):
    pass



