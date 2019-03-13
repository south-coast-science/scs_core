"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

all:
site,data_status,action_code,datetime,parameter,duration,frequency,value,unit_code,qc_code,poc,
lat,lon,GISdatum,elev,method_code,mpc,mpc_value,uncertainty,qualifiers

first time / mobile:
site,data_status,,datetime,parameter,duration,,value,unit_code,qc_code,poc,
lat1,lon1,,,,,,,

subsequent:
site,data_status,,datetime,parameter,duration,,value,unit_code,qc_code,poc,
,,,,,,,,

https://www.airnow.gov/
"""

from collections import OrderedDict

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime
from scs_core.aqcsv.data.aqcsv_site import AQCSVSite

from scs_core.aqcsv.specification.method import Method
from scs_core.aqcsv.specification.mpc import MPC
from scs_core.aqcsv.specification.parameter import Parameter
from scs_core.aqcsv.specification.qc import QC
from scs_core.aqcsv.specification.unit import Unit

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVRecord(JSONable):
    """
    classdocs
    """

    STATUS_PRELIMINARY =        0
    STATUS_FINAL =              1

    ACTION_DEFAULT =            0
    ACTION_INSERT_AUTO =        1
    ACTION_UPDATE_AUTO =        2
    ACTION_INSERT_NOAUTO =      3
    ACTION_UPDATE_NOAUTO =      4
    ACTION_DELETE =             5

    GIS_DATUM =                 "WGS84"


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fixed_int(value, fmt):
        try:
            return fmt % int(value)
        except ValueError:
            return value


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        site_code = jdict.get('site')
        data_status = jdict.get('data_status')

        action_code = jdict.get('action_code')

        datetime_code = jdict.get('datetime')
        parameter_code = jdict.get('parameter')
        duration = jdict.get('duration')

        frequency = jdict.get('frequency')

        value = jdict.get('value')
        unit_code = jdict.get('unit')
        qc_code = jdict.get('qc')
        poc = jdict.get('poc')

        lat = jdict.get('lat')
        lon = jdict.get('lon')
        gis_datum = jdict.get('GISDatum')
        elev = jdict.get('elev')

        method_code = jdict.get('method_code')
        mpc_code = jdict.get('mpc')
        mpc_value = jdict.get('mpc_value')
        uncertainty = jdict.get('uncertainty')
        qualifiers = jdict.get('qualifiers')

        return AQCSVRecord(site_code=site_code, data_status=data_status, action_code=action_code,
                           datetime_code=datetime_code, parameter_code=parameter_code, duration=duration,
                           frequency=frequency, value=value, unit_code=unit_code, qc_code=qc_code, poc=poc,
                           lat=lat, lon=lon, gis_datum=gis_datum, elev=elev, method_code=method_code,
                           mpc_code=mpc_code, mpc_value=mpc_value, uncertainty=uncertainty, qualifiers=qualifiers)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site_code=None, data_status=None, action_code=None,
                 datetime_code=None, parameter_code=None, duration=None,
                 frequency=None, value=None, unit_code=None, qc_code=None, poc=None,
                 lat=None, lon=None, gis_datum=None, elev=None, method_code=None,
                 mpc_code=None, mpc_value=None, uncertainty=None, qualifiers=None):
        """
        Constructor
        """
        self.__site_code = str(site_code)                           # nvarchar(12)      required
        self.__data_status = Datum.int(data_status)                 # int(1)            required

        self.__action_code = Datum.int(action_code)                 # int(1)

        self.__datetime_code = str(datetime_code)                   # nvarchar(20)      required
        self.__parameter_code = parameter_code                      # int(5) or string  required
        self.__duration = Datum.int(duration)                       # int               required

        self.__frequency = Datum.int(frequency)                     # int

        self.__value = Datum.float(value, 5)                        # numeric(10,5)     required
        self.__unit_code = Datum.int(unit_code)                     # int(3)            required
        self.__qc_code = Datum.int(qc_code)                         # int               required
        self.__poc = Datum.int(poc)                                 # int               required

        self.__lat = Datum.float(lat, 6)                            # numeric(10,6)
        self.__lon = Datum.float(lon, 6)                            # numeric(10,6)
        self.__gis_datum = gis_datum                                # nvarchar(10)
        self.__elev = Datum.int(elev)                               # int

        self.__method_code = Datum.int(method_code)                 # int(3)
        self.__mpc_code = Datum.int(mpc_code)                       # int
        self.__mpc_value = Datum.float(mpc_value, 5)                # numeric(10,5)
        self.__uncertainty = Datum.float(uncertainty, 5)            # numeric(10,5)
        self.__qualifiers = qualifiers                              # nvarchar(255)


    def __eq__(self, other):
        try:
            return \
                self.site_code == other.site_code and \
                self.data_status == other.data_status and \
                self.action_code == other.action_code and \
                self.datetime_code == other.datetime_code and \
                self.parameter_code == other.parameter_code and \
                self.duration == other.duration and \
                self.frequency == other.frequency and \
                self.value == other.value and \
                self.unit_code == other.unit_code and \
                self.qc_code == other.qc_code and \
                self.poc == other.poc and \
                self.lat == other.lat and \
                self.lon == other.lon and \
                self.gis_datum == other.gis_datum and \
                self.elev == other.elev and \
                self.method_code == other.method_code and \
                self.mpc_code == other.mpc_code and \
                self.mpc_value == other.mpc_value and \
                self.uncertainty == other.uncertainty and \
                self.qualifiers == other.qualifiers

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['site'] = self.site_code
        jdict['data_status'] = self.data_status

        jdict['action_code'] = self.action_code

        jdict['datetime'] = self.datetime_code
        jdict['parameter'] = self.fixed_int(self.parameter_code, "%05d")
        jdict['duration'] = self.duration

        jdict['frequency'] = self.frequency

        jdict['value'] = self.value
        jdict['unit'] = self.fixed_int(self.unit_code, "%03d")
        jdict['qc'] = self.qc_code
        jdict['poc'] = self.poc

        jdict['lat'] = self.lat
        jdict['lon'] = self.lon
        jdict['GISDatum'] = self.gis_datum
        jdict['elev'] = self.elev

        jdict['method_code'] = self.fixed_int(self.method_code, "%03d")
        jdict['mpc'] = self.mpc_code
        jdict['mpc_value'] = self.mpc_value
        jdict['uncertainty'] = self.uncertainty
        jdict['qualifiers'] = self.qualifiers

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def site(self):
        return AQCSVSite.construct_from_code(self.site_code)


    def datetime(self):
        return AQCSVDatetime.construct_from_code(self.datetime_code)


    def parameter(self):
        return Parameter.instance(self.parameter_code)


    def unit(self):
        return Unit.instance(self.unit_code)


    def qc(self):
        return QC.instance(self.qc_code)


    def method(self):
        return Method.instance((self.parameter_code, self.method_code))


    def mpc(self):
        return MPC.instance(self.mpc_code)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def site_code(self):
        return self.__site_code


    @property
    def data_status(self):
        return self.__data_status


    @property
    def action_code(self):
        return self.__action_code


    @property
    def datetime_code(self):
        return self.__datetime_code


    @property
    def parameter_code(self):
        return self.__parameter_code


    @property
    def duration(self):
        return self.__duration


    @property
    def frequency(self):
        return self.__frequency


    @property
    def value(self):
        return self.__value


    @property
    def unit_code(self):
        return self.__unit_code


    @property
    def qc_code(self):
        return self.__qc_code


    @property
    def poc(self):
        return self.__poc


    @property
    def lat(self):
        return self.__lat


    @property
    def lon(self):
        return self.__lon


    @property
    def gis_datum(self):
        return self.__gis_datum


    @property
    def elev(self):
        return self.__elev


    @property
    def method_code(self):
        return self.__method_code


    @property
    def mpc_code(self):
        return self.__mpc_code


    @property
    def mpc_value(self):
        return self.__mpc_value


    @property
    def uncertainty(self):
        return self.__uncertainty


    @property
    def qualifiers(self):
        return self.__qualifiers


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVRecord:{site_code:%s, data_status:%1d, action_code:%s, datetime_code:%s, parameter_code:%s, " \
               "duration:%d, frequency:%s, value:%0.5f, unit_code:%03d, qc_code:%d, poc:%d, " \
               "lat:%s, lon:%s, gis_datum:%s, elev:%s, method_code:%s, mpc_code:%s, mpc_value:%s, " \
               "uncertainty:%s, qualifiers:%s}" % \
               (self.site_code, self.data_status, self.action_code, self.datetime_code, self.parameter_code,
                self.duration, self.frequency, self.value, self.unit_code, self.qc_code, self.poc,
                self.lat, self.lon, self.gis_datum, self.elev, self.method_code, self.mpc_code, self.mpc_value,
                self.uncertainty, self.qualifiers)


# --------------------------------------------------------------------------------------------------------------------

class AQCSVFirstRecord(AQCSVRecord):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site_code, data_status, datetime_code, parameter_code, duration, value, unit_code,
                 qc_code, poc, lat, lon):
        """
        Constructor
        """
        super().__init__(site_code=site_code, data_status=data_status, datetime_code=datetime_code,
                         parameter_code=parameter_code, duration=duration, value=value, unit_code=unit_code,
                         qc_code=qc_code, poc=poc, lat=lat, lon=lon)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVFirstRecord:{site_code:%s, data_status:%1d, datetime_code:%s, parameter_code:%05d, " \
               "duration:%d, value:%0.5f, unit_code:%03d, qc_code:%d, poc:%d, lat:%0.6f, lon:%0.6f}" % \
               (self.site_code, self.data_status, self.datetime_code, self.parameter_code,
                self.duration, self.value, self.unit_code, self.qc_code, self.poc, self.lat, self.lon)


# --------------------------------------------------------------------------------------------------------------------

class AQCSVSubsequentRecord(AQCSVRecord):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site_code, data_status, datetime_code, parameter_code, duration, value, unit_code,
                 qc_code, poc):
        """
        Constructor
        """
        super().__init__(site_code=site_code, data_status=data_status, datetime_code=datetime_code,
                         parameter_code=parameter_code, duration=duration, value=value, unit_code=unit_code,
                         qc_code=qc_code, poc=poc)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVSubsequentRecord:{site_code:%s, data_status:%1d, datetime_code:%s, parameter_code:%05d, " \
               "duration:%d, value:%0.5f, unit_code:%03d, qc_code:%d, poc:%d}" % \
               (self.site_code, self.data_status, self.datetime_code, self.parameter_code,
                self.duration, self.value, self.unit_code, self.qc_code, self.poc)
