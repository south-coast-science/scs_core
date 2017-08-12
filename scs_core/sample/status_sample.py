"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class StatusSample(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, timezone, position, temperature, schedule, uptime, psu_status):
        """
        Constructor
        """
        val = []

        if timezone:
            val.append(('tz', timezone))

        if position:
            val.append(('pos', position))

        val.append(('sch', schedule))
        val.append(('tmp', temperature))
        val.append(('up', uptime))

        if psu_status:
            val.append(('psu', psu_status))

        super().__init__(tag, rec, *val)
