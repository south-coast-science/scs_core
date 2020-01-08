"""
Created on 7 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A CSV-friendly grid that can be used to visualise the scaling error predicted for a given OPC exegete, by PM size,
using any rH range or resolution.
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.particulate.exegesis.exegete import Exegete


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRendering(JSONable):
    """
    classdocs
    """

    PRECISION = 3

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, rh_min, rh_max, rh_delta, exegete: Exegete):
        rows = [ExegeteRenderingRow.construct(species, rh_min, rh_max, rh_delta, exegete)
                for species in ('pm1', 'pm2p5', 'pm10')]

        return ExegeteRendering(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rows):
        """
        Constructor
        """
        self.__rows = rows                          # array of ExegeteRenderingRow


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        report = []

        for row in self.__rows:
            report.append(row.as_json())

        return report


    # ----------------------------------------------------------------------------------------------------------------

    def rows(self):
        for row in self.__rows:
            yield row


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        rows = '[' + ', '.join(str(row) for row in self.__rows) + ']'

        return "ExegeteRendering:{rows:%s}" % rows


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingRow(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, species, rh_min, rh_max, rh_delta, exegete: Exegete):
        cells = [ExegeteRenderingCell(rh, exegete.error(species, rh))
                 for rh in range(rh_min, rh_max + 1, rh_delta)]

        return ExegeteRenderingRow(species, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, species, cells):
        """
        Constructor
        """
        self.__species = species                    # string
        self.__cells = cells                        # array of ExegeteRenderingCell


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['species'] = self.species

        for cell in self.cells():
            jdict[cell.key()] = round(cell.error, ExegeteRendering.PRECISION)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def species(self):
        return self.__species


    def cells(self):
        for cell in self.__cells:
            yield cell


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cells = '[' + ', '.join(str(cell) for cell in self.__cells) + ']'

        return "ExegeteRendering:{species:%s, cells:%s}" %  (self.species, cells)


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingCell(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh, error):
        """
        Constructor
        """
        self.__rh = rh                              # numeric
        self.__error = error                        # float


    # ----------------------------------------------------------------------------------------------------------------

    def key(self):
        return str(self.rh) + ' %'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh(self):
        return self.__rh


    @property
    def error(self):
        return self.__error


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ExegeteRenderingCell:{rh:%s, error:%0.1f}" % (self.rh, self.error)
