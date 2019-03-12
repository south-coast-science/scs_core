"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"topic": "particulates", "species": "pm2p5"}
"""

from collections import OrderedDict

from scs_core.aqcsv.connector.status_mapping import StatusMapping
from scs_core.aqcsv.connector.source_mapping import SourceMapping

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime
from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class DatumMapping(JSONable):
    """
    classdocs
    """

    __SCHEDULES = {
        'gases': 'scs-gases',
        'particulates': 'scs-particulates'
    }

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        topic = jdict.get('topic')
        species = jdict.get('species')

        return DatumMapping(topic, species)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def aqcsv_rec(datum: PathDict):
        localised = LocalizedDatetime.construct_from_jdict(datum.node('rec'))
        timezone = StatusMapping.timezone(datum)

        return AQCSVDatetime.construct_from_localised_datetime(localised, timezone)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, species):
        """
        Constructor
        """
        self.__topic = topic                                        # string
        self.__species = species                                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['species'] = self.species

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def aqcsv_record(self, datum: PathDict):
        # common components...
        aqcsv_source = self.aqcsv_source(datum)

        if aqcsv_source is None:
            return None

        site_conf = StatusMapping.site_conf(datum)

        if site_conf is None:
            return None

        # parameters...
        site_code = site_conf.site.as_code()

        data_status = AQCSVRecord.STATUS_FINAL
        action_code = AQCSVRecord.ACTION_DEFAULT

        aqcsv_rec = self.aqcsv_rec(datum)
        datetime_code = aqcsv_rec.as_json()

        parameter_code = aqcsv_source.parameter_code

        duration = self.duration(datum)

        value = self.value(datum)
        unit_code = aqcsv_source.unit_code

        qc_code = aqcsv_source.qc_code
        poc = site_conf.poc(parameter_code)

        gps = StatusMapping.gps(datum)

        if gps is not None:
            lat = gps.pos.lat
            lon = gps.pos.lng
            gis_datum = AQCSVRecord.GIS_DATUM
            elev = round(gps.elv)

        else:
            lat = None
            lon = None
            gis_datum = None
            elev = None

        method_code = aqcsv_source.method_code
        mpc_code = aqcsv_source.mpc_code
        mpc_value = aqcsv_source.mpc_value

        # record...
        record = AQCSVRecord(
            site_code=site_code,
            data_status=data_status,
            action_code=action_code,
            datetime_code=datetime_code,
            parameter_code=parameter_code,
            duration=duration,
            frequency=None,
            value=value,
            unit_code=unit_code,
            qc_code=qc_code,
            poc=poc,
            lat=lat,
            lon=lon,
            gis_datum=gis_datum,
            elev=elev,
            method_code=method_code,
            mpc_code=mpc_code,
            mpc_value=mpc_value,
            uncertainty=None,
            qualifiers=None)

        return record


    # ----------------------------------------------------------------------------------------------------------------

    def aqcsv_source(self, datum: PathDict):
        pk = (self.topic, self.species, self.source(datum))

        return SourceMapping.instance(pk)


    def tag(self, datum: PathDict):
        tag_path = '.'.join([self.topic, 'tag'])

        return datum.node(tag_path)


    def value(self, datum: PathDict):
        species_path = '.'.join([self.topic, 'val', self.species])

        return datum.node(species_path)


    def source(self, datum: PathDict):
        source_path = '.'.join([self.topic, 'src'])

        return datum.node(source_path)


    def duration(self, datum: PathDict):
        schedule_path = '.'.join(['status.val.sch', self.__SCHEDULES[self.topic]])
        schedule = datum.node(schedule_path)

        return int(schedule['interval']) * int(schedule['tally'])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def species(self):
        return self.__species


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DatumMapping:{topic:%s, species:%s}" % (self.topic, self.species)
