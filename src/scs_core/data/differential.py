"""
Created on 16 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class Differential(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, prec=1):
        """
        Constructor
        """
        self.__prec = prec

        self.__prev_x = None
        self.__prev_y = None


    # ----------------------------------------------------------------------------------------------------------------

    def slope(self, x, y):
        if self.__prev_x is None:
            slope = None

        else:
            delta_x = x - self.__prev_x
            delta_y = y - self.__prev_y
            slope = round(delta_y / delta_x, self.__prec)

        self.__prev_x = x
        self.__prev_y = y

        return slope


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def prev_x(self):
        return self.__prev_x


    @property
    def prev_y(self):
        return self.__prev_y


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Differential:{prev_x:%s, prev_y:%s, prec:%s}" % (self.prev_x, self.prev_y, self.__prec)
