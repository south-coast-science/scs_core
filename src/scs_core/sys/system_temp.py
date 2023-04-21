"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SystemTemp(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        board = jdict.get('brd')
        host = jdict.get('hst')

        return cls(board, host)


    @classmethod
    def construct(cls, board_datum, host_datum):
        board = None if board_datum is None else board_datum.temp
        host = None if host_datum is None else host_datum.temp

        return cls(board, host)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, board, host):
        """
        Constructor
        """
        self.__board = board
        self.__host = host                                          # PersistenceManager


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['brd'] = self.board

        if self.host is not None:
            jdict['hst'] = self.host

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def board(self):
        return self.__board


    @property
    def host(self):
        return self.__host


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SystemTemp:{board:%s, host:%s}" % (self.board, self.host)
