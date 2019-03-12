"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.data.path_dict import PathDict

from scs_core.location.timezone import Timezone

from scs_core.position.gps_datum import GPSDatum


# --------------------------------------------------------------------------------------------------------------------

class StatusMapping(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def tag(cls, datum: PathDict):
        return datum.node('status.tag')


    @classmethod
    def site_conf(cls, datum: PathDict):
        jdict = datum.node('status.val.airnow')

        return AirNowSiteConf.construct_from_jdict(jdict)


    @classmethod
    def gps(cls, datum: PathDict):
        jdict = datum.node('status.val.gps')

        return GPSDatum.construct_from_jdict(jdict)


    @classmethod
    def timezone(cls, datum: PathDict):
        jdict = datum.node('status.val.tz')

        return Timezone.construct_from_jdict(jdict)
