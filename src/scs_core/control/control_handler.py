"""
Created on 11 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import sys

from scs_core.control.control_receipt import ControlReceipt


# --------------------------------------------------------------------------------------------------------------------

class ControlHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__outgoing_pub = None                      # Publication
        self.__receipt = None                           # ControlReceipt


    # ----------------------------------------------------------------------------------------------------------------

    def set(self, outgoing_pub):
        self.__outgoing_pub = outgoing_pub
        self.__receipt = None


    def handle(self, _client, _userdata, message):
        print("handle - message: %s" % message, file=sys.stderr)
        payload = json.loads(message.payload.decode())

        try:
            receipt = ControlReceipt.construct_from_jdict(payload)
        except TypeError:
            return

        if receipt.tag == self.__outgoing_pub.payload.attn and receipt.omd == self.__outgoing_pub.payload.digest:
            self.__receipt = receipt


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def receipt(self):
        return self.__receipt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlHandler:{outgoing_pub:%s, receipt:%s}" %  (self.__outgoing_pub, self.receipt)
