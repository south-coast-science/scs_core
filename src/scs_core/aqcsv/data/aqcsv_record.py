"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

all:
site,data_status,action_code,datetime,parameter,duration,frequency,value,unit,qc,poc,
lat,lon,GISdatum,elev,method_code,mpc,mpc_value,uncertainty,qualifiers

first time / mobile:
site,data_status,,datetime1,parameter,duration,,value,unit,qc,poc,lat1,lon1,,,,,,,

subsequent...
site,data_status,,datetime,parameter,duration,,value,unit,qc,poc,,,,,,,,,
"""

from collections import OrderedDict

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVRecord(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        site = jdict.get('site')
        data_status = jdict.get('data_status')

        action_code = jdict.get('action_code')

        datetime_code = jdict.get('datetime')
        parameter = jdict.get('parameter')
        duration = jdict.get('duration')

        frequency = jdict.get('frequency')

        value = jdict.get('value')
        unit = jdict.get('unit')
        qc = jdict.get('qc')
        poc = jdict.get('poc')

        lat = jdict.get('lat')
        lon = jdict.get('lon')
        gis_datum = jdict.get('GISdatum')
        elev = jdict.get('elev')

        method_code = jdict.get('method_code')
        mpc = jdict.get('mpc')
        mpc_value = jdict.get('mpc_value')
        uncertainty = jdict.get('uncertainty')
        qualifiers = jdict.get('qualifiers')

        return AQCSVRecord(site=site, data_status=data_status, action_code=action_code, datetime_code=datetime_code,
                           parameter=parameter, duration=duration, frequency=frequency, value=value, unit=unit, qc=qc,
                           poc=poc, lat=lat, lon=lon, gis_datum=gis_datum, elev=elev, method_code=method_code,
                           mpc=mpc, mpc_value=mpc_value, uncertainty=uncertainty, qualifiers=qualifiers)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site=None, data_status=None, action_code=None, datetime_code=None, parameter=None,
                 duration=None, frequency=None, value=None, unit=None, qc=None,
                 poc=None, lat=None, lon=None, gis_datum=None, elev=None,
                 method_code=None, mpc=None, mpc_value=None, uncertainty=None, qualifiers=None):
        """
        Constructor
        """
        self.__site = site                                      # nvarchar(12)
        self.__data_status = data_status                        # int(1)

        self.__action_code = action_code                        # int(1)

        self.__datetime_code = datetime_code                    # nvarchar(20)
        self.__parameter = parameter                            # int(5)
        self.__duration = duration                              # int

        self.__frequency = frequency                            # int

        self.__value = value                                    # numeric(10,5)
        self.__unit = unit                                      # int(3)
        self.__qc = qc                                          # int
        self.__poc = poc                                        # int

        self.__lat = lat                                        # numeric(10,6)
        self.__lon = lon                                        # numeric(10,6)
        self.__gis_datum = gis_datum                            # nvarchar(10)
        self.__elev = elev                                      # int

        self.__method_code = method_code                        # nvarchar(3)
        self.__mpc = mpc                                        # int
        self.__mpc_value = mpc_value                            # numeric(10,5)
        self.__uncertainty = uncertainty                        # numeric(10,5)
        self.__qualifiers = qualifiers                          # nvarchar(255)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return \
            self.site == other.site and \
            self.data_status == other.data_status and \
            self.action_code == other.action_code and \
            self.datetime_code == other.datetime_code and \
            self.parameter == other.parameter and \
            self.duration == other.duration and \
            self.frequency == other.frequency and \
            self.value == other.value and \
            self.unit == other.unit and \
            self.qc == other.qc and \
            self.poc == other.poc and \
            self.lat == other.lat and \
            self.lon == other.lon and \
            self.gis_datum == other.gis_datum and \
            self.elev == other.elev and \
            self.method_code == other.method_code and \
            self.mpc == other.mpc and \
            self.mpc_value == other.mpc_value and \
            self.uncertainty == other.uncertainty and \
            self.qualifiers == other.qualifiers


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['site'] = self.site
        jdict['data_status'] = self.data_status

        jdict['action_code'] = self.action_code

        jdict['datetime'] = self.datetime_code
        jdict['parameter'] = self.parameter
        jdict['duration'] = self.duration

        jdict['frequency'] = self.frequency

        jdict['value'] = self.value
        jdict['unit'] = self.unit
        jdict['qc'] = self.qc
        jdict['poc'] = self.poc

        jdict['lat'] = self.lat
        jdict['lon'] = self.lon
        jdict['GISdatum'] = self.gis_datum
        jdict['elev'] = self.elev

        jdict['method_code'] = self.method_code
        jdict['mpc'] = self.mpc
        jdict['mpc_value'] = self.mpc_value
        jdict['uncertainty'] = self.uncertainty
        jdict['qualifiers'] = self.qualifiers

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def datetime(self):
        return AQCSVDatetime.construct_from_code(self.datetime_code)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def site(self):
        return self.__site


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
    def parameter(self):
        return self.__parameter


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
    def unit(self):
        return self.__unit


    @property
    def qc(self):
        return self.__qc


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
    def mpc(self):
        return self.__mpc


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
        return "AQCSVRecord:{site:%s, data_status:%s, action_code:%s, datetime_code:%s, parameter:%s, " \
               "duration:%s, frequency:%s, value:%s, unit:%s, qc:%s, " \
               "poc:%s, lat:%s, lon:%s, gis_datum:%s, elev:%s, " \
               "method_code:%s, code:%s, mpc_value:%s, uncertainty:%s, qualifiers:%s}" % \
               (self.site, self.data_status, self.action_code, self.datetime_code, self.parameter,
                self.duration, self.frequency, self.value, self.unit, self.qc,
                self.poc, self.lat, self.lon, self.gis_datum, self.elev,
                self.method_code, self.mpc, self.mpc_value, self.uncertainty, self.qualifiers)


# --------------------------------------------------------------------------------------------------------------------

class AQCSVFirstRecord(AQCSVRecord):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site, data_status, datetime_code, parameter, duration, value, unit, qc, poc, lat, lon):
        """
        Constructor
        """
        super().__init__(site=site, data_status=data_status, datetime_code=datetime_code, parameter=parameter,
                         duration=duration, value=value, unit=unit, qc=qc, poc=poc, lat=lat, lon=lon)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVFirstRecord:{site:%s, data_status:%s, datetime_code:%s, parameter:%s, " \
               "duration:%s, value:%s, unit:%s, qc:%s, poc:%s, lat:%s, lon:%s}" % \
               (self.site, self.data_status, self.datetime_code, self.parameter,
                self.duration, self.value, self.unit, self.qc, self.poc, self.lat, self.lon)


# --------------------------------------------------------------------------------------------------------------------

class AQCSVSubsequentRecord(AQCSVRecord):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, site, data_status, datetime_code, parameter, duration, value, unit, qc, poc):
        """
        Constructor
        """
        super().__init__(site=site, data_status=data_status, datetime_code=datetime_code, parameter=parameter,
                         duration=duration, value=value, unit=unit, qc=qc, poc=poc)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVSubsequentRecord:{site:%s, data_status:%s, datetime_code:%s, parameter:%s, " \
               "duration:%s, value:%s, unit:%s, qc:%s, poc:%s}" % \
               (self.site, self.data_status, self.datetime_code, self.parameter,
                self.duration, self.value, self.unit, self.qc, self.poc)
