"""
Created on 21 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-be2-3", "rec": "2018-06-21T16:13:52.675+00:00", "val": {"pA": 102.2, "p0": 113.8, "tmp": 25.6}}
"""

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class PressureSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, mpl115a2_datum):
        """
        Constructor
        """
        val = [('pA', mpl115a2_datum.actual_press)]

        if mpl115a2_datum.sl_press is not None:
            val.append(('p0', mpl115a2_datum.sl_press))

        if mpl115a2_datum.temp is not None:
            val.append(('tmp', mpl115a2_datum.temp))

        super().__init__(tag, rec, *val)
