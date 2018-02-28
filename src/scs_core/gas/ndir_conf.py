"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not an NDIR is present

example JSON:
{"present": true}
"""


# TODO: make stub NDIRConf compatible with the real one

# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(object):
    """
    A stub class for an NDIR that may be implemented elsewhere
    """

    @classmethod
    def load(cls, _):
        return NDIRConf()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def ndir(cls, _):
        return None


    @property
    def present(self):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf:{present:False}"
