"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.data.path_dict import PathDict

from scs_core.location.timezone import Timezone

from scs_core.position.gps_datum import GPSDatum


# --------------------------------------------------------------------------------------------------------------------

class DeviceMapping(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def tag(cls, datum: PathDict):
        return datum.node(cls.tag_path())


    @classmethod
    def site(cls, datum: PathDict):
        jdict = datum.node(cls.site_path())

        return AirNowSiteConf.construct_from_jdict(jdict)


    @classmethod
    def timezone(cls, datum: PathDict):
        jdict = datum.node(cls.timezone_path())

        return Timezone.construct_from_jdict(jdict)


    @classmethod
    def gps(cls, datum: PathDict):
        jdict = datum.node(cls.gps_path())

        return GPSDatum.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def tag_path():
        return 'status.tag'


    @staticmethod
    def site_path():
        return 'status.val.airnow'


    @staticmethod
    def timezone_path():
        return 'status.val.tz'


    @staticmethod
    def gps_path():
        return 'status.val.gps'
