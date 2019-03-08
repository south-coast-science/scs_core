"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Site information required for a device that may join the AirNow-I project

example JSON:
"""

from collections import OrderedDict

from scs_core.aqcsv.data.aqcsv_site import AQCSVSite

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class AirNowSiteConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "airnow_site_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        site = AQCSVSite.construct_from_code(jdict.get('site'))
        pocs = jdict.get('pocs')

        return AirNowSiteConf(site, pocs)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site, pocs):
        """
        Constructor
        """
        super().__init__()

        self.__site = site                                  # AQCSVSite
        self.__pocs = pocs                                  # dictionary of parameter: code


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['site'] = None if self.site is None else self.site.as_code()
        jdict['pocs'] = self.pocs

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def poc(self, parameter):
        if parameter not in self.__pocs:
            return 1

        return self.__pocs[parameter]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def site(self):
        return self.__site


    @property
    def pocs(self):
        return self.__pocs


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AirNowSiteConf:{site:%s, pocs:%s}" %  (self.site, self.pocs)
