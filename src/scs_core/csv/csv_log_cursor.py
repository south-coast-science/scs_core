"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://dbader.org/blog/queues-in-python
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CSVLogCursorList(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        cursors = OrderedDict()

        for cursor_jdict in jdict.get('cursors'):
            cursor = CSVLogCursor.construct_from_jdict(cursor_jdict)
            cursors[cursor.file_path] = cursor

        return cls(cursors)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cursors):
        """
        Constructor
        """
        self.__cursors = cursors                        # OrderedDict of file_path: LogCursor


    def __len__(self):
        return len(self.__cursors)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['cursors'] = [cursor.as_json() for cursor in self.__cursors.values()]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def include(self, file_path, row_number=0):
        if file_path not in self.__cursors:
            self.__cursors[file_path] = CSVLogCursor(file_path, row_number)


    def pop(self):
        try:
            return self.__cursors.popitem()[1]

        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cursors = '[' + ', '.join(str(cursor) for cursor in self.__cursors.values()) + ']'

        return "CSVLogCursorList:{cursors:%s}" %  cursors


# --------------------------------------------------------------------------------------------------------------------

class CSVLogCursor(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        file_path = jdict.get('file-path')
        row_number = jdict.get('row-number')

        return cls(file_path, row_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, file_path, row_number):
        """
        Constructor
        """
        self.__file_path = file_path                            # string
        self.__row_number = int(row_number)                     # int


    def __eq__(self, other):
        return self.file_path == other.file_path


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['file-path'] = self.file_path
        jdict['row-number'] = self.row_number

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def file_path(self):
        return self.__file_path


    @property
    def row_number(self):
        return self.__row_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogCursor:{file_path:%s, row_number:%s}" %  (self.file_path, self.row_number)
