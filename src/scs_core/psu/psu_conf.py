"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU board is present, if any

example JSON:
{"model": "OsloV1"}
"""


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(object):
    """
    A stub class for a PSU that may be implemented elsewhere
    """

    @classmethod
    def load(cls, _):
        return PSUConf()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def psu(cls, _):
        return None


    @classmethod
    def psu_monitor(cls, _):
        return None


    @property
    def model(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf:{model:None}"
