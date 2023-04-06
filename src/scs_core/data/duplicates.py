"""
Created on 2 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json


# --------------------------------------------------------------------------------------------------------------------

class Duplicates(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__matches = {}
        self.__max_index = 0


    # ----------------------------------------------------------------------------------------------------------------

    def test(self, index, key, value):
        jstr = json.dumps(key)

        # test...
        if jstr in self.__matches:
            is_duplicate = True

        else:
            self.__matches[jstr] = {}
            is_duplicate = False

        # store..
        self.__matches[jstr][index] = value

        if index > self.__max_index:
            self.__max_index = index

        # report...
        return is_duplicate


    # ----------------------------------------------------------------------------------------------------------------

    def matched_keys(self):
        for key in self.keys:
            if len(self.__matches[key]) > 1:
                yield key


    def match_counts(self):
        for key in self.matched_keys():
            yield {key: len(self.__matches[key])}


    def matches(self):
        for key in self.matched_keys():
            yield {key: self.__matches[key]}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def keys(self):
        return sorted(self.__matches.keys())


    @property
    def key_count(self):
        return len(self.__matches)


    @property
    def matched_key_count(self):
        count = 0

        for key in self.__matches:
            if len(self.__matches[key]) > 1:
                count += 1

        return count


    @property
    def total_matches(self):
        count = 0

        for key in self.__matches:
            if len(self.__matches[key]) > 1:
                count += len(self.__matches[key])

        return count


    @property
    def max_index(self):
        return self.__max_index


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Duplicates:{max_index:%s, keys:%s, matched_key_count:%s}" % \
               (self.max_index, self.key_count, self.matched_key_count)
