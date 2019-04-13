"""
Created on 12 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only use this on data sets where there are no missing timeline intervals!
"""

from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class NodeShifter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, offset, fill, source_sub_path, target_sub_path=None):
        """
        Constructor
        """
        self.__offset = offset                                                                      # int
        self.__fill = fill                                                                          # bool

        self.__source_sub_path = source_sub_path                                                    # string
        self.__target_sub_path = source_sub_path if target_sub_path is None else target_sub_path    # string

        self.__documents = []                                                                       # array of PathDict
        self.__enqueued = 0                                                                         # int


    def __len__(self):
        return len(self.__documents)


    # ----------------------------------------------------------------------------------------------------------------

    def shift(self, document: PathDict):
        self.append(document)

        return self.pop()


    def append(self, document: PathDict):
        self.__documents.append(document)
        self.__enqueued += 1


    def pop(self):
        length = len(self)

        if length == 0:
            return None

        # indices...
        if self.offset > 0:
            outer_index = length - self.enqueued
            inner_index = outer_index - self.offset

        else:
            inner_index = length - self.enqueued
            outer_index = inner_index + self.offset

        # sources...
        outer = self.__documents[outer_index] if outer_index in range(length) else None
        inner = self.__documents[inner_index] if inner_index in range(length) else None

        self.__enqueued -= 1

        # trim the list...
        if outer is not None and inner is not None:
            del self.__documents[0]

        # check...
        if outer is None:
            return None

        if inner is None and not self.fill:
            return None

        # target...
        document = PathDict()

        for source_path in outer.paths():
            if PathDict.sub_path_includes_path(self.source_sub_path, source_path):
                source = inner
                path = source_path.replace(self.source_sub_path, self.target_sub_path)

            else:
                source = outer
                path = source_path

            node = None if source is None else source.node(source_path)

            document.append(path, node)

        return document


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def offset(self):
        return self.__offset


    @property
    def fill(self):
        return self.__fill


    @property
    def source_sub_path(self):
        return self.__source_sub_path


    @property
    def target_sub_path(self):
        return self.__target_sub_path


    @property
    def enqueued(self):
        return self.__enqueued


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NodeShifter:{offset:%s, fill:%s, source_sub_path:%s, target_sub_path:%s, enqueued:%s, len:%s}" % \
               (self.offset, self.fill, self.source_sub_path, self.target_sub_path, self.enqueued, len(self))
