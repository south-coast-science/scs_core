"""
Created on 5 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class MonitorRequest(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        group = jdict.get('grp')
        command = jdict.get('cmd')
        params = jdict.get('params')

        return MonitorRequest(group, command, params)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group, command, params):
        """
        Constructor
        """
        self.__group = group
        self.__command = command
        self.__params = params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group(self):
        return self.__group


    @property
    def command(self):
        return self.__command


    @property
    def params(self):
        return self.__params


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MonitorRequest:{group:%s, command:%s, params:%s}" % (self.group, self.command, self.params)
