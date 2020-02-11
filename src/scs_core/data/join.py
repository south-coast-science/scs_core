"""
Created on 22 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.w3schools.com/sql/sql_join.asp
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class Join(object):
    """
    classdocs
    """

    TYPES = {'INNER', 'LEFT', 'RIGHT', 'FULL'}

    @classmethod
    def is_valid_type(cls, name):
        return name.upper() in cls.TYPES


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, left_set_path, left_pk_path, right_set_path, right_pk_path, pk_is_iso8601):
        left = JoinSet(left_set_path, left_pk_path, pk_is_iso8601)
        right = JoinSet(right_set_path, right_pk_path, pk_is_iso8601)

        return Join(left, right)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, left, right):
        """
        Constructor
        """
        self.__left = left                      # JoinSet
        self.__right = right                    # JoinSet


    # ----------------------------------------------------------------------------------------------------------------

    def append_to_left(self, document: PathDict):
        self.__left.append(document)


    def append_to_right(self, document: PathDict):
        self.__right.append(document)


    # ----------------------------------------------------------------------------------------------------------------

    def inner(self):
        # paths...
        pk_path = self.__left.pk_path
        right_path = self.__right.set_path
        left_path = self.__left.set_path

        # join...
        for pk in self.__left.pk_values():
            right = self.__right.retrieve(pk)

            if right is None:
                continue

            left = self.__left.retrieve(pk)

            yield PathDict.union((pk_path, pk), (left_path, left), (right_path, right))


    def left(self):
        # paths...
        pk_path = self.__left.pk_path
        right_path = self.__right.set_path
        left_path = self.__left.set_path

        # join...
        for pk in self.__left.pk_values():
            right = self.__right.retrieve(pk)
            left = self.__left.retrieve(pk)

            yield PathDict.union((pk_path, pk), (left_path, left), (right_path, right))


    def right(self):
        # paths...
        pk_path = self.__right.pk_path
        right_path = self.__right.set_path
        left_path = self.__left.set_path

        # join...
        for pk in self.__right.pk_values():
            right = self.__right.retrieve(pk)
            left = self.__left.retrieve(pk)

            yield PathDict.union((pk_path, pk), (left_path, left), (right_path, right))


    def full(self):
        # paths...
        pk_path = self.__left.pk_path
        right_path = self.__right.set_path
        left_path = self.__left.set_path

        # keys...
        right_pk_values = set(self.__right.pk_values())
        left_pk_values = set(self.__left.pk_values())

        pk_values = sorted(right_pk_values | left_pk_values)

        # join...
        for pk in pk_values:
            right = self.__right.retrieve(pk)
            left = self.__left.retrieve(pk)

            yield PathDict.union((pk_path, pk), (left_path, left), (right_path, right))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Join:{left:%s, right:%s}" % (self.__left, self.__right)


# --------------------------------------------------------------------------------------------------------------------

class JoinSet(object):
    """
    classdocs
    """

    def __init__(self, set_path, pk_path, pk_is_iso8601):
        """
        Constructor
        """
        self.__set_path = set_path
        self.__pk_path = pk_path
        self.__pk_is_iso8601 = pk_is_iso8601

        self.__documents = {}


    def __len__(self):
        return len(self.__documents)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, document: PathDict):
        pk_value = document.node(self.pk_path)

        if self.pk_is_iso8601:
            datetime = LocalizedDatetime.construct_from_iso8601(pk_value)

            if datetime is None:
                raise ValueError(pk_value)

            pk_value = datetime

        self.__documents[pk_value] = document


    # ----------------------------------------------------------------------------------------------------------------

    def pk_values(self):
        for pk_value in self.__documents.keys():
            yield pk_value


    def retrieve(self, pk_value):
        try:
            document = self.__documents[pk_value]
        except KeyError:
            return None

        node = PathDict()

        for path in document.paths():
            if path != self.pk_path:
                node.append(path, document.node(path))

        return node


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set_path(self):
        return self.__set_path


    @property
    def pk_path(self):
        return self.__pk_path


    @property
    def pk_is_iso8601(self):
        return self.__pk_is_iso8601


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "JoinSet:{set_path:%s, pk_path:%s, pk_is_iso8601:%s, len:%d}" % \
               (self.set_path, self.pk_path, self.pk_is_iso8601, len(self))
