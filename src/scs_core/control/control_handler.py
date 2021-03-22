"""
Created on 11 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.control.control_receipt import ControlReceipt


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


    # ----------------------------------------------------------------------------------------------------------------

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
