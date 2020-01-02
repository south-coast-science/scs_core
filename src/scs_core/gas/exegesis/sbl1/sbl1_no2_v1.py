"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from reference data at LHR2 in 2019.
"""

import json

from scs_core.error.error_surface import ErrorSurface
from scs_core.gas.exegesis.sbl1.sbl1 import SBL1


# --------------------------------------------------------------------------------------------------------------------

class SBL1NO2v1(SBL1):
    """
    classdocs
    """

    __NAME =             'sbl1no2v1'

    __STANDARD_SURFACE = '{"mt_weights": [-0.002171, 0.343086, -13.826], "ct_weights": [0.042619, -6.21781, 244.445]}'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def standard(cls):
        surface = ErrorSurface.construct_from_jdict(json.loads(cls.__STANDARD_SURFACE))

        return cls(surface)
