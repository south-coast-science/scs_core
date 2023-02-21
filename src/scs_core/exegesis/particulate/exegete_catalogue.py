"""
Created on 25 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an empty catalogue of particulate exegesis models, to be implemented elsewhere
"""


# --------------------------------------------------------------------------------------------------------------------

class ExegeteCatalogue(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def model_names():
        return tuple()


    @staticmethod
    def load(_name, _host):
        raise NotImplementedError


    @staticmethod
    def standard(_name):
        raise NotImplementedError
