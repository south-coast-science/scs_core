"""
Created on 09 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class EmailList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_email_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        email_list = jdict.get('email_list')

        return EmailList(email_list)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_list):
        """
        Constructor
        """
        self.__email_list = email_list

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email_list(self):
        return self.__email_list

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email_list'] = self.__email_list

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EmailList:{email_list:%s}" %  \
               self.__email_list
