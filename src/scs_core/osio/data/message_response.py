"""
Created on 7 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class MessageResponse(object):
    """
    classdocs
    """

    __SEND_SUCCESS =      'Message sent'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        message = jdict.get('message')

        return MessageResponse(message)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message):
        """
        Constructor
        """
        self.__message = message                # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_ok(self):
        return self.__message == MessageResponse.__SEND_SUCCESS


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def message(self):
        return self.__message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{message:%s}" % self.message
