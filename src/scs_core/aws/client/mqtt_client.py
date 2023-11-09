"""
Created on 6 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/aws/aws-iot-device-sdk-python
https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/sphinx/html/index.html

https://github.com/aws/aws-iot-device-sdk-python/issues/57

https://stackoverflow.com/questions/20083858/how-to-extract-value-from-bound-method-in-python

https://github.com/aws/aws-iot-device-sdk-python-V2
https://github.com/aws/aws-iot-device-sdk-java/issues/2
"""

import logging
import time

from AWSIoTPythonSDK.exception.AWSIoTExceptions import connectError, connectTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import disconnectError, disconnectTimeoutException

import AWSIoTPythonSDK.MQTTLib as MQTTLib

from scs_core.aws.client.client_auth import ClientAuth

from scs_core.data.json import JSONify
from scs_core.data.str import Str

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class MQTTClient(object):
    """
    classdocs
    """
    __KEEP_ALIVE_INTERVAL =         1200                   # recommended: 30 default: 600 (seconds)

    __PORT =                        8883

    __QUEUE_SIZE =                  -1                      # recommended: infinite
    __QUEUE_DROP_BEHAVIOUR =        MQTTLib.DROP_OLDEST     # not required for infinite queue
    __QUEUE_DRAINING_FREQUENCY =    2                       # recommended: 2 (Hz)

    __RECONN_BASE =                 1                       # recommended: 1 (sec)
    __RECONN_MAX =                  10                      # recommended: 32 or 128 (sec), was 5
    __RECONN_STABLE =               5                       # recommended: 20 (sec), was 10

    __DISCONNECT_TIMEOUT =          60                      # recommended: 10 (sec), was 40
    __OPERATION_TIMEOUT =           60                      # recommended: 5 (sec), was 20

    __PUB_QOS =                     1
    __SUB_QOS =                     1


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __assert_logger(level):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(level)
        logger.addHandler(stream_handler)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *subscribers):
        """
        Constructor
        """
        self.__client = None
        self.__subscribers = subscribers


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, auth, debug=False):
        # logging...
        if debug:
            self.__assert_logger(logging.DEBUG)

        # client...
        self.__client = MQTTLib.AWSIoTMQTTClient(auth.client_id)

        # configuration...
        self.__client.configureEndpoint(auth.endpoint, self.__PORT)

        self.__client.configureCredentials(auth.root_ca_file_path, auth.private_key_path, auth.certificate_path)

        self.__client.configureAutoReconnectBackoffTime(self.__RECONN_BASE, self.__RECONN_MAX, self.__RECONN_STABLE)

        self.__client.configureOfflinePublishQueueing(self.__QUEUE_SIZE)
        self.__client.configureDrainingFrequency(self.__QUEUE_DRAINING_FREQUENCY)

        self.__client.configureConnectDisconnectTimeout(self.__DISCONNECT_TIMEOUT)
        self.__client.configureMQTTOperationTimeout(self.__OPERATION_TIMEOUT)

        # subscriptions...
        for subscriber in self.__subscribers:
            self.__client.subscribe(subscriber.topic, self.__SUB_QOS, subscriber.handler)

        # connect...
        try:
            return self.__client.connect(keepAliveIntervalSecond=self.__KEEP_ALIVE_INTERVAL)

        except (connectError, connectTimeoutException) as ex:
            raise OSError(repr(ex))


    def disconnect(self):
        if self.__client is None:
            return

        try:
            self.__client.disconnect()

        except (disconnectError, disconnectTimeoutException):
            pass

        self.__client = None


    # --------------------------------------------------------------------------------------------------------------------

    def publish(self, publication):
        if not self.__client:
            raise IOError("publish: no client")

        payload = JSONify.dumps(publication.payload)

        return self.__client.publish(publication.topic, payload, self.__PUB_QOS)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTClient:{subscribers:%s}" % Str.collection(self.__subscribers)


# --------------------------------------------------------------------------------------------------------------------

class MQTTClientManager(object):
    """
    a singleton class, because the MQTTClient cannot be pickled (and the the MQTTClient must be unique)
    """

    __WAIT_FOR_CONNECTION_TIME = 10         # seconds

    __AUTH = None
    __CLIENT = None

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def configure(cls, auth: ClientAuth, client: MQTTClient):
        """
        Constructor
        """
        cls.__AUTH = auth
        cls.__CLIENT = client


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def network_not_available_handler(cls):
        Logging.getLogger().error("network loss - attempting to reconnect MQTT client")

        cls.disconnect()                    # remove dead connection
        cls.connect()


    @classmethod
    def connect(cls):
        while True:
            try:
                cls.__CLIENT.connect(cls.__AUTH, debug=Logging.debugging_on())        # connect when possible
                Logging.getLogger().info("connected")
                break
            except OSError:
                time.sleep(cls.__WAIT_FOR_CONNECTION_TIME)


    @classmethod
    def disconnect(cls):
        if cls.__CLIENT:
            cls.__CLIENT.disconnect()
            Logging.getLogger().info("disconnected")


# --------------------------------------------------------------------------------------------------------------------

class MQTTSubscriber(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, handler):
        """
        Constructor
        """
        self.__topic = topic
        self.__handler = handler


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def handler(self):
        return self.__handler


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTSubscriber:{topic:%s, handler:%s}" % (self.topic, self.handler.__self__)
