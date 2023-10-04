"""
Created on 22 Feb 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import json
import logging
import requests
import time

from collections import OrderedDict
from AWSIoTPythonSDK.exception import operationError, operationTimeoutException

from scs_core.aws.client.client_auth import ClientAuth
from scs_core.aws.client.mqtt_client import MQTTClient, MQTTSubscriber

from scs_core.aws.manager.byline.byline import TopicBylineGroup
from scs_core.aws.manager.dynamo_manager import DynamoManager

from scs_core.control.control_datum import ControlDatum
from scs_core.control.control_handler import ControlHandler

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.publication import Publication

from scs_core.estate.configuration import Configuration


# ----------------------------------------------------------------------------------------------------------------

class MQTTDevicePoller(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __DEVICE_TOPICS_URL = 'https://xy1eszuu23.execute-api.us-west-2.amazonaws.com/dev/device-topics'

    __BUCKET = "scs-persistence"
    __KEY = "conf/mqtt_peers.json"
    __TABLE = "device_configuration"

    __TIMEOUT = 30          # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, s3_manager, dynamo_client=None, dynamo_resource=None):
        """
        Constructor
        """
        self.__host = host                                          # PersistenceManager
        self.__s3_manager = s3_manager
        self.__dynamo_manager = DynamoManager(dynamo_client, dynamo_resource) if dynamo_client and dynamo_resource \
            else None

        self.__logger = logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def all_devices(cls):
        req = requests.get(cls.__DEVICE_TOPICS_URL)
        status = req.status_code
        if status != 200:
            return None

        res = req.content
        jdict = json.loads(res)

        group = TopicBylineGroup.construct_from_jdict(jdict, excluded="/control")

        return group.devices


    def known_devices(self, with_info=False):
        # TODO: replace the below with load(..) method
        res, _ = self.__s3_manager.retrieve_from_bucket(self.__BUCKET, self.__KEY)
        json_data = json.loads(res)
        data = json_data["peers"]

        known_dev = []

        if not with_info:
            for item in data.items():
                tag = item[1]["tag"]
                known_dev.append(tag)
        else:
            for item in data.items():
                data = item[1]
                known_dev.append(data)

        return known_dev


    def missing_devices(self):
        missing_dev = set(self.all_devices()) - set(self.known_devices())

        return sorted(missing_dev)


    # ----------------------------------------------------------------------------------------------------------------

    def update_configs(self):
        jdict = OrderedDict()

        for device in self.known_devices(with_info=True):
            d_tag = device["tag"]
            d_ss = device["shared-secret"]
            d_topic = device["topic"]
            res = self.send_mqtt(d_tag, d_ss, d_topic, "?")

            jdict[d_tag] = res
            print("Device:%s :%s" % (d_tag, res))
            self.__logger.info("Device:%s :%s" % (d_tag, res))

            if res != "Timeout":
                if "configuration" in res[0]:
                    self.get_configuration(d_tag, d_ss, d_topic)


    def get_configuration(self, device_tag, shared_secret, topic):
        tokens = ["configuration"]
        print(type(tokens))
        res = self.send_mqtt(device_tag, shared_secret, topic, tokens)
        self.save_changes(device_tag, res)


    def send_mqtt(self, device_tag, d_ss, d_topic, token):
        # tag...
        host_tag = self.__host.name()

        # ClientAuth...
        auth = ClientAuth.load(self.__host)

        if auth is None:
            # log no auth
            exit(1)

        # responder...
        handler = ControlHandler(host_tag, device_tag)

        subscriber = MQTTSubscriber(d_topic, handler.handle)
        client = MQTTClient(subscriber)

        # go
        client.connect(auth)

        # datum...
        now = LocalizedDatetime.now().utc()
        datum = ControlDatum.construct(host_tag, device_tag, now, token, self.__TIMEOUT, d_ss)

        publication = Publication(d_topic, datum)

        handler.set_outgoing(publication)

        try:
            client.publish(publication)

        except (OSError, operationError, operationTimeoutException) as ex:
            self.__logger.error(repr(ex))

        timeout = time.time() + self.__TIMEOUT

        while True:
            if handler.receipt:
                if not handler.receipt.is_valid(d_ss):
                    client.disconnect()
                    raise ValueError("invalid digest: %s" % handler.receipt)

                if handler.receipt.command.stderr:
                    client.disconnect()
                    return handler.receipt.command.stderr

                if handler.receipt.command.stdout:
                    client.disconnect()
                    return handler.receipt.command.stdout

            if time.time() > timeout:  # was cmd.interactive and ...
                client.disconnect()
                return "Timeout"

            time.sleep(0.1)


    def save_changes(self, device_tag, response):
        # see if item already in DB

        current = self.__dynamo_manager.items(self.__TABLE, "device_tag", device_tag)
        if current:
            loaded = current[0]['data'][0]
            res_str = response[0]
            loaded_conf = Configuration.construct_from_jstr(loaded)
            this_conf = Configuration.construct_from_jstr(res_str)
            if loaded_conf == this_conf:
                # config remains the same, delete original compo key & replace to avoid clutter
                key = {
                    'device_tag': current[0]['device_tag'],
                    'datetime': current[0]['datetime']
                }

                self.__dynamo_manager.delete_item(self.__TABLE, key)

        # add to db
        item = {
            'device_tag': device_tag,
            'datetime': LocalizedDatetime.now().as_iso8601(),
            'data': response
        }

        self.__dynamo_manager.add(self.__TABLE, item)


