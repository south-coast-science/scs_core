"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import sys

from getpass import getpass


# --------------------------------------------------------------------------------------------------------------------

class AccessKeys(object):
    """
    classdocs
    """

    ID_NAME = 'AWS_ACCESS_KEY_ID'
    SECRET_NAME = 'AWS_SECRET_ACCESS_KEY'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def get(cls):
        if cls.ID_NAME in os.environ:
            access_key_id = os.environ[cls.ID_NAME]
        else:
            print("Enter AWS Access Key: ", file=sys.stderr)
            access_key_id = input()

        if cls.SECRET_NAME in os.environ:
            access_key_secret = os.environ[cls.SECRET_NAME]
        else:
            print("Enter Secret AWS Access Key: ", file=sys.stderr)
            access_key_secret = getpass()

        return access_key_id, access_key_secret
