"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"topic": "particulates", "species": "pm1", "site-code": null}
"""

from collections import OrderedDict

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.aqcsv.connector.source_mapping import SourceMapping

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime
from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict

from scs_core.location.timezone import Timezone

from scs_core.position.gps_datum import GPSDatum


# --------------------------------------------------------------------------------------------------------------------

class DatumMapping(JSONable):
    """
    classdocs
    """

    __SCHEDULES = {
        'gases': 'scs-gases',
        'particulates': 'scs-particulates'
    }

    @classmethod
    def is_valid_topic(cls, topic):
        return topic in cls.__SCHEDULES


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        topic = jdict.get('topic')
        species = jdict.get('species')
        site_code = jdict.get('site-code')

        return DatumMapping(topic, species, site_code)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, species, site_code=None):
        """
        Constructor
        """
        self.__topic = topic                                        # string
        self.__species = species                                    # string
        self.__site_code = site_code                                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['species'] = self.species
        jdict['site-code'] = self.site_code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def aqcsv_record(self, datum: PathDict, duration):
        # validate...
        if self.environment_tag(datum) != self.status_tag(datum):
            raise ValueError("non-matching tag fields: %s" % datum)

        # parameter_code...
        mapping = self.aqcsv_source_mapping(datum)
        parameter_code = mapping.parameter_code

        # site_code / POCs...
        if self.__site_code is not None:
            code = self.__site_code
            poc = 1

        else:
            site_conf = self.site_conf(datum)
            code = site_conf.site.as_code()
            poc = site_conf.poc(parameter_code)

        # datetime_code...
        rec = self.aqcsv_rec(datum)

        # position...
        gps = self.gps(datum)

        if gps is not None and gps.elv is not None:
            lat = gps.pos.lat
            lon = gps.pos.lng
            gis_datum = AQCSVRecord.GIS_DATUM
            elev = int(round(gps.elv))

        else:
            lat = None
            lon = None
            gis_datum = None
            elev = None

        # record...
        record = AQCSVRecord(
            site_code=code,

            data_status=AQCSVRecord.STATUS_FINAL,
            action_code=AQCSVRecord.ACTION_DEFAULT,

            datetime_code=rec.as_json(),

            parameter_code=parameter_code,

            duration=duration,
            frequency=0,

            value=self.value(datum),
            unit_code=mapping.unit_code,

            qc_code=mapping.qc_code,
            poc=poc,

            lat=lat,
            lon=lon,
            gis_datum=gis_datum,
            elev=elev,

            method_code=mapping.method_code,
            mpc_code=mapping.mpc_code,
            mpc_value=mapping.mpc_value)

        return record


    # ----------------------------------------------------------------------------------------------------------------
    # environment fields...

    def environment_tag(self, datum: PathDict):
        tag_path = '.'.join([self.topic, 'tag'])

        return datum.node(tag_path)


    def aqcsv_rec(self, datum: PathDict):
        localised = LocalizedDatetime.construct_from_jdict(datum.node('rec'))
        timezone = self.timezone(datum)

        return AQCSVDatetime(localised.datetime, timezone.zone)


    def aqcsv_source_mapping(self, datum: PathDict):
        pk = (self.topic, self.species, self.source(datum))

        mapping = SourceMapping.instance(pk)

        if mapping is None:
            raise KeyError("no source mapping found for %s" % str(pk))

        return mapping


    def value(self, datum: PathDict):
        species_path = '.'.join([self.topic, 'val', self.species])

        return datum.node(species_path)


    def source(self, datum: PathDict):
        source_path = '.'.join([self.topic, 'src'])

        return datum.node(source_path)


    # ----------------------------------------------------------------------------------------------------------------
    # status fields...

    @classmethod
    def status_tag(cls, datum: PathDict):
        return datum.node('status.tag')


    @classmethod
    def site_conf(cls, datum: PathDict):
        jdict = datum.node('status.val.airnow')

        conf = AirNowSiteConf.construct_from_jdict(jdict)

        if conf is None:
            raise KeyError("no site configuration found for %s" % str(jdict))

        return conf


    @classmethod
    def gps(cls, datum: PathDict):
        jdict = datum.node('status.val.gps')

        return GPSDatum.construct_from_jdict(jdict)


    @classmethod
    def timezone(cls, datum: PathDict):
        jdict = datum.node('status.val.tz')

        return Timezone.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def species(self):
        return self.__species


    @property
    def site_code(self):
        return self.__site_code


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DatumMapping:{topic:%s, species:%s, site_code:%s}" % (self.topic, self.species, self.site_code)
