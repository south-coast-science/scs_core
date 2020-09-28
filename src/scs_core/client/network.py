"""
Created on 27 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from subprocess import Popen


# --------------------------------------------------------------------------------------------------------------------

class Network(object):
    """
    classdocs
    """
    __TEST_RESOURCE =       'google.com'
    __NETWORK_WAIT_TIME =   5.0                         # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def wait(cls):
        cls.wait_for_resource(cls.__TEST_RESOURCE)


    @classmethod
    def wait_for_resource(cls, resource):
        while not cls.resource_is_available(resource):
            time.sleep(cls.__NETWORK_WAIT_TIME)


    @classmethod
    def resource_is_available(cls, resource):
        with open(os.devnull, 'wb') as devnull:
            return Popen(['ping', '-c', '1', resource], stdout=devnull, stderr=devnull).wait() == 0
