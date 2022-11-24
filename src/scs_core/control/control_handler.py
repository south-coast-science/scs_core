"""
Created on 11 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import time

from AWSIoTPythonSDK.exception.operationError import operationError
from AWSIoTPythonSDK.exception.operationTimeoutException import operationTimeoutException

from scs_core.control.control_datum import ControlDatum
from scs_core.control.control_receipt import ControlReceipt

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.publication import Publication

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ControlHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host_tag, device_tag):
        """
        Constructor
        """
        self.__host_tag = host_tag                      # string
        self.__device_tag = device_tag                  # string

        self.__outgoing_pub = None                      # ControlDatum
        self.__receipt = None                           # ControlReceipt

        self.__logger = Logging.getLogger()             # Logger


    # ----------------------------------------------------------------------------------------------------------------

    def publish(self, client, topic, cmd_tokens, cmd_timeout, key):
        now = LocalizedDatetime.now().utc()
        str_tokens = [str(token) for token in cmd_tokens]

        # datum...
        datum = ControlDatum.construct(self.__host_tag, self.__device_tag, now, str_tokens, cmd_timeout, key)

        publication = Publication(topic, datum)
        self.set_outgoing(publication)

        self.__logger.info(datum)

        # publish...
        try:
            success = client.publish(publication)
            self.__logger.info("paho: %s" % "1" if success else "0")

        except (OSError, operationError, operationTimeoutException) as ex:
            self.__logger.error(repr(ex))
            exit(1)

        # subscribe...
        timeout = time.time() + cmd_timeout

        while True:
            if self.receipt:
                if not self.receipt.is_valid(key):
                    raise ValueError("invalid digest: %s" % self.receipt)

                self.__logger.info(self.receipt)

                return self.receipt.command.stdout, self.receipt.command.stderr,  self.receipt.command.return_code

            if time.time() > timeout:
                raise TimeoutError(cmd_timeout)

            time.sleep(0.1)


    def set_outgoing(self, outgoing_pub):
        self.__outgoing_pub = outgoing_pub
        self.__receipt = None


    def handle(self, _client, _userdata, message):
        payload = json.loads(message.payload.decode())

        try:
            receipt = ControlReceipt.construct_from_jdict(payload)
        except TypeError:
            return

        if receipt.tag != self.__device_tag:
            return

        if receipt.attn is not None and receipt.attn != self.__host_tag:
            return

        if receipt.omd != self.__outgoing_pub.payload.digest:
            return

        self.__receipt = receipt


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def receipt(self):
        return self.__receipt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlHandler:{host_tag:%s, device_tag:%s, outgoing_pub:%s, receipt:%s}" %  \
               (self.__host_tag, self.__device_tag, self.__outgoing_pub, self.receipt)
