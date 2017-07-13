"""
Created on 6 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

co-ordinated with scs_core.sys.DeviceID message_tag() method

example:
scs-pfa-3
"""

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MessageTag(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        fields = jdict.split('-')

        vendor_id = fields[0]
        model_id = fields[1]
        serial_number = int(fields[2])
        signature = None                    # fields[3]

        return MessageTag(vendor_id, model_id, serial_number, signature)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, vendor_id, model_id, serial_number, signature):
        """
        Constructor
        """
        self.__vendor_id = vendor_id                # string (3 chars)
        self.__model_id = model_id                  # string (3 chars)
        self.__serial_number = serial_number        # int
        self.__signature = signature                # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, message):
        print("sig: %s msg: %s" % (self.signature, message))
        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.vendor_id + '-' + self.model_id + '-' + self.serial_number + '-' + self.signature


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor_id(self):
        return self.__vendor_id


    @property
    def model_id(self):
        return self.__model_id


    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def signature(self):
        return self.__signature


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageTag:{vendor_id:%s, model_id:%s, serial_number:%s, signature:%s}" % \
               (self.vendor_id, self.model_id, self.serial_number, self.signature)
