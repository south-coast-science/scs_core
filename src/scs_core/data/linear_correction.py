"""
Created on 24 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class LinearCorrection(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, start_datetime, delta_x_datetime, delta_y):
        initial_x = start_datetime.timestamp()
        final_x = delta_x_datetime.timestamp()

        delta_x = final_x - initial_x

        return LinearCorrection(initial_x, delta_x, delta_y)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, initial_x, delta_x, delta_y):
        """
        Constructor
        """
        self.__initial_x = initial_x            # timestamp
        self.__delta_x = delta_x                # timestamp

        self.__delta_y = delta_y                # number


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, datum_x, datum_y):
        x_offset = (datum_x - self.__initial_x) / self.__delta_x
        y_offset =  self.__delta_y * x_offset

        return datum_y + y_offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinearCorrection:{initial_x:%s, delta_x:%s, delta_y:%s}" % \
               (self.__initial_x, self.__delta_x, self.__delta_y)
