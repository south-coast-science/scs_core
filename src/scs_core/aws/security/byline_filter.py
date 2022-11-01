"""
Created on 31 Oct 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class BylineFilter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, user_paths):
        """
        Constructor
        """
        self.__user_paths = user_paths                  # array of string


    # ----------------------------------------------------------------------------------------------------------------

    def filter(self, bylines):
        for byline in bylines:
            topic = byline['topic']

            for user_path in self.__user_paths:
                if topic.startswith(user_path):
                    yield byline
                    break


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def user_paths(self):
        return self.__user_paths


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineFilter:{user_paths:%s}" % self.user_paths
