"""
Created on 31 Oct 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------
class PathFilter(object):
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

    def byline_filter(self, bylines):
        for byline in bylines:
            topic = byline['topic']

            for user_path in self.__user_paths:
                if topic.startswith(user_path):
                    yield byline
                    break


    def device_is_visible(self, pod):
        for user_path in self.__user_paths:
            if pod.device_path.startswith(user_path) or pod.location_path.startswith(user_path):
                return True

        return False


    def path_is_visible(self, path):
        for user_path in self.__user_paths:
            if path.startswith(user_path):
                return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def user_paths(self):
        return self.__user_paths


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PathFilter:{user_paths:%s}" % self.user_paths
