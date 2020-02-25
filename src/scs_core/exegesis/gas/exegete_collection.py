"""
Created on 25 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an empty collection of gas exegesis models, to be implemented elsewhere
"""


# --------------------------------------------------------------------------------------------------------------------

class ExegeteCollection(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, _exegete_names):
        return cls()


    # ----------------------------------------------------------------------------------------------------------------

    def __len__(self):
        return 0


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def has_member(_name):
        return False


    @staticmethod
    def has_members():
        return False


    @staticmethod
    def uses_external_sht():
        return False


    @staticmethod
    def interpretation(_text, _internal_sht_sample, _external_sht_sample):
        return {}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ExegeteCollection:{}"
