"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note that, for the ISO 8601 constructors, milliseconds are optional.

http://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/
https://stackoverflow.com/questions/6410971/python-datetime-object-show-wrong-timezone-offset

https://docs.microsoft.com/en-us/dotnet/api/system.datetime.tooadate?view=netframework-4.8
http://code.activestate.com/recipes/496683-converting-ole-datetime-values-into-python-datetim/
"""

import pytz
import re
import tzlocal

from datetime import date, datetime, timedelta, timezone

from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# TODO: object should carry a flag indicating presence of millis - for "preserve millis" mode?
# --------------------------------------------------------------------------------------------------------------------

class LocalizedDatetime(JSONable):
    """
    classdocs
    """

    UNIX_ERA_START = '1970-01-01T00:00:00Z'

    OLE_TIME_ZERO = datetime(1899, month=12, day=30)

    MONTH_NAMES = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    @classmethod
    def month(cls, name):
        try:
            return cls.MONTH_NAMES[name.lower()]
        except KeyError:
            raise ValueError(name)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def now(cls):
        zone = tzlocal.get_localzone()
        localized = datetime.now(zone)

        return LocalizedDatetime(localized)


    @classmethod
    def unix_era_start(cls):
        return cls.construct_from_iso8601(cls.UNIX_ERA_START)


    @classmethod
    def construct_from_date(cls, d):
        zone = tzlocal.get_localzone()
        localized = zone.localize(datetime(d.year, month=d.month, day=d.day))

        return LocalizedDatetime(localized)


    @classmethod
    def construct_from_timestamp(cls, t, tz=None):
        zone = tzlocal.get_localzone() if tz is None else tz
        localized = datetime.fromtimestamp(t, zone)

        return LocalizedDatetime(localized)


    @classmethod
    def construct_from_iso8601(cls, datetime_str):
        if datetime_str is None:
            return None

        # Z timezone offset...
        localized = cls.__construct_from_iso8601_z(datetime_str)

        if localized:
            return localized

        # numeric timezone offset...
        return cls.__construct_from_iso8601_numeric(datetime_str)


    @classmethod
    def construct_from_date_time(cls, date_parser, date_str, time_str, tz=None):
        # date...
        d = date_parser.datetime(date_str)

        if d is None:
            return None

        # time (rightmost time in string)...
        match = re.match(r'(\d{1,2}):(\d{2})(:(\d{2}))? *([APap][Mm])? *$', time_str)       # e.g. 24:00:00

        if match is None:
            return None

        fields = match.groups()

        hours_delta = int(fields[0])
        minutes_delta = int(fields[1])
        seconds_delta = 0 if fields[3] is None else int(fields[3])

        if fields[4] == 'pm' or fields[4] == 'PM':
            hours_delta += 12

        # zone...
        zone = pytz.timezone('Etc/UTC') if tz is None else tz

        # construct...
        start = LocalizedDatetime(zone.localize(d))

        corrected = start.timedelta(seconds=seconds_delta, minutes=minutes_delta, hours=hours_delta)

        return corrected


    @classmethod
    def construct_from_aws(cls, datetime_str):
        if datetime_str is None:
            return None

        iso_datetime_str = datetime_str.replace(' ', 'T')

        return cls.__construct_from_iso8601_numeric(iso_datetime_str)


    @classmethod
    def construct_from_s3(cls, datetime_str):       # Sat, 11 Sep 2021 08:47:47 GMT
        # match...
        match = re.match(r'\S{3}, (\d{1,2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT', datetime_str)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[2])
        month = cls.month(fields[1])
        day = int(fields[0])

        hour = int(fields[3])
        minute = int(fields[4])
        second = int(fields[5])

        # construct...
        zone_offset = timedelta()
        zone = timezone(zone_offset)

        localized = datetime(year, month=month, day=day, hour=hour, minute=minute, second=second, tzinfo=zone)

        return LocalizedDatetime(localized)


    @classmethod
    def construct_from_oad(cls, oad, tz=None):
        d = cls.OLE_TIME_ZERO + timedelta(days=float(oad))

        # zone...
        zone = pytz.timezone('Etc/UTC') if tz is None else tz

        # construct...
        return LocalizedDatetime(zone.localize(d))


    @classmethod
    def construct_from_jdict(cls, jdict):               # TODO: deprecated
        return cls.construct_from_iso8601(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __construct_from_iso8601_z(cls, datetime_str):
        # match...
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:.(\d{3,6}))?Z', datetime_str)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])

        hour = int(fields[3])
        minute = int(fields[4])
        second = int(fields[5])

        if fields[6]:
            multiplier = 1000 if len(fields[6]) == 3 else 1
            micros = int(fields[6]) * multiplier
        else:
            micros = 0

        # construct...
        zone_offset = timedelta()
        zone = timezone(zone_offset)

        localized = datetime(year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=micros,
                             tzinfo=zone)

        return LocalizedDatetime(localized)


    @classmethod
    def __construct_from_iso8601_numeric(cls, datetime_str):
        # match...
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:.(\d{3,6}))?([ +\-]?)(\d{2}):(\d{2})',
                         datetime_str)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])

        hour = int(fields[3])
        minute = int(fields[4])
        second = int(fields[5])

        if fields[6]:
            multiplier = 1000 if len(fields[6]) == 3 else 1
            micros = int(fields[6]) * multiplier
        else:
            micros = 0

        zone_sign = -1 if fields[7] == '-' else 1
        zone_hours = int(fields[8])
        zone_mins = int(fields[9])

        # construct...
        zone_offset = zone_sign * timedelta(hours=zone_hours, minutes=zone_mins)
        zone = timezone(zone_offset)

        localized = datetime(year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=micros,
                             tzinfo=zone)

        return LocalizedDatetime(localized)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, localized):
        """
        Constructor
        """
        self.__datetime = localized                     # datetime


    def __hash__(self):
        return hash(self.datetime)


    def __eq__(self, other):
        try:
            return self.datetime == other.datetime

        except AttributeError:
            return False


    def __ge__(self, other):
        return self.datetime >= other.datetime


    def __gt__(self, other):
        return self.datetime > other.datetime


    def __le__(self, other):
        return self.datetime <= other.datetime


    def __lt__(self, other):
        return self.datetime < other.datetime


    def __add__(self, other):
        if type(other) == Timedelta:
            return LocalizedDatetime(self.datetime + other.delta)

        if type(other) == timedelta:
            return LocalizedDatetime(self.datetime + other)

        raise TypeError(other)


    def __sub__(self, other):
        if type(other) == LocalizedDatetime:
            return Timedelta.construct(self.datetime - other.datetime)

        if type(other) == datetime:
            return Timedelta.construct(self.datetime - other)

        if type(other) == Timedelta:
            return LocalizedDatetime(self.datetime - other.delta)

        if type(other) == timedelta:
            return LocalizedDatetime(self.datetime - other)

        raise TypeError(other)


    def __round__(self, n=3):
        if not 0 <= n <= 3:
            raise ValueError(n)

        rounded = self.__datetime

        # second...
        if round(rounded.microsecond / 1000000):
            rounded += timedelta(seconds=1, microseconds=-rounded.microsecond)
        else:
            rounded -= timedelta(microseconds=rounded.microsecond)

        # minute...
        if n < 3:
            if round(rounded.second / 60):
                rounded += timedelta(minutes=1, seconds=-rounded.second)
            else:
                rounded -= timedelta(seconds=rounded.second)

        # hour...
        if n < 2:
            if round(rounded.minute / 60):
                rounded += timedelta(hours=1, minutes=-rounded.minute)
            else:
                rounded -= timedelta(minutes=rounded.minute)

        # day...
        if n < 1:
            if round(rounded.hour / 24):
                rounded += timedelta(days=1, hours=-rounded.hour)
            else:
                rounded -= timedelta(hours=rounded.hour)

        return LocalizedDatetime(rounded)


    # ----------------------------------------------------------------------------------------------------------------

    def utc(self):
        localized = self.datetime.astimezone(pytz.timezone('Etc/UTC'))

        return LocalizedDatetime(localized)


    def localize(self, zone):                           # zone may be datetime.timezone or pytz.timezone
        localized = self.datetime.astimezone(zone)

        return LocalizedDatetime(localized)


    def timedelta(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        td = timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds,
                       minutes=minutes, hours=hours, weeks=weeks)

        return LocalizedDatetime(self.__datetime + td)


    def dst(self):
        return Timedelta.construct(self.__datetime.dst())


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.as_iso8601()


    def as_iso8601(self, include_millis=False):
        """
        example: 2016-08-13T00:38:05.210+01:00
        """
        d = self.__datetime.strftime("%Y-%m-%d")
        t = self.__datetime.strftime("%H:%M:%S")

        # millis...
        if include_millis:
            micros = float(self.__datetime.strftime("%f"))
            millis = ".%03d" % (micros // 1000)

        else:
            millis = ""

        # time zone...
        zone = self.__datetime.strftime("%z")

        # Z format...
        if float(zone[1:]) == 0.0:
            return "%sT%s%sZ" % (d, t, millis)

        # numeric format...
        zone_hours = zone[:3]
        zone_mins = zone[3:]

        return "%sT%s%s%s:%s" % (d, t, millis, zone_hours, zone_mins)


    def as_time(self):
        t = self.__datetime.strftime("%H:%M:%S")

        micros = float(self.__datetime.strftime("%f"))
        millis = "%03d" % (micros // 1000)

        return "%s.%s" % (t, millis)


    def timestamp(self):
        return self.__datetime.timestamp()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def datetime(self):
        return self.__datetime


    @property
    def utc_datetime(self):
        utc_localised = self.utc()

        return utc_localised.datetime


    @property
    def tzinfo(self):
        return self.__datetime.tzinfo


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LocalizedDatetime:{datetime:%s}" % self.datetime


# --------------------------------------------------------------------------------------------------------------------

class Date(object):
    """
    classdocs
    """

    @classmethod
    def is_valid_iso_format(cls, date_str):
        try:
            date.fromisoformat(date_str)
            return True

        except (TypeError, ValueError):
            return False


# --------------------------------------------------------------------------------------------------------------------

class DateParser(object):
    """
    classdocs
    """

    __FORMATS = {
        'DD-MM-YYYY': ('%d-%m-%Y', False),
        'DD/MM/YYYY': ('%d/%m/%Y', False),
        'DD/MM/YY': ('%d/%m/%y', False),
        'MM-DD-YYYY': ('%m-%d-%Y', False),
        'MM/DD/YYYY': ('%m/%d/%Y', False),
        'MM/DD/YY': ('%m/%d/%y', False),
        'YYYY-MM-DD': ('%Y-%m-%d', False),
        'YYYY/MM/DD': ('%Y/%m/%d', False),
        'DD_MMM_YYYY': ('%d %m %Y', True)
    }

    __MONTHS = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }


    @classmethod
    def formats(cls):
        return sorted(cls.__FORMATS.keys())


    @classmethod
    def is_valid_format(cls, date_format):
        return date_format in cls.__FORMATS.keys()


    @classmethod
    def construct(cls, date_format):
        strptime_format, textual_month = cls.__FORMATS[date_format]

        return cls(strptime_format, textual_month)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, strptime_format, textual_month):
        """
        Constructor
        """
        self.__strptime_format = strptime_format
        self.__textual_month = textual_month


    # ----------------------------------------------------------------------------------------------------------------

    def datetime(self, datetime_str):
        try:
            if self.__textual_month:
                month_name = self.__month_name(datetime_str)
                standard_datetime = datetime_str.replace(month_name, self.__MONTHS[month_name])
            else:
                standard_datetime = datetime_str

            return datetime.strptime(standard_datetime, self.__strptime_format)

        except (KeyError, TypeError, ValueError):
            return None


    @staticmethod
    def __month_name(datetime_str):
        pieces = datetime_str.split(' ')

        for piece in pieces:
            if len(piece) == 3:
                return piece

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DateParser:{format:%s, textual_month:%s}" % (self.__strptime_format, self.__textual_month)


# --------------------------------------------------------------------------------------------------------------------

class ISO8601(object):
    """
    classdocs
    """

    @classmethod
    def construct(cls, localised_datetime):
        if localised_datetime is None:
            return None

        iso8601 = localised_datetime.as_iso8601(True)

        if iso8601 is None:
            return None

        iso = cls.__parse_z(iso8601)
        if iso:
            return iso

        return cls.__parse_numeric(iso8601)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __parse_z(cls, iso8601):
        # 2016-08-13T00:38:05.210Z
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:.(\d{3}))?Z', iso8601)

        if match is None:
            return None

        fields = match.groups()

        year = fields[0]
        month = fields[1]
        day = fields[2]

        hour = fields[3]
        minute = fields[4]
        second = fields[5]
        millis = fields[6]

        tz_sign = '+'
        tz_hour = '00'
        tz_minute = '00'

        return cls(year, month, day, hour, minute, second, millis, tz_sign, tz_hour, tz_minute)


    @classmethod
    def __parse_numeric(cls, iso8601):
        # 2016-08-13T00:38:05.210+01:00
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3})([+-])(\d{2}):(\d{2})', iso8601)

        if match is None:
            return None

        fields = match.groups()

        year = fields[0]
        month = fields[1]
        day = fields[2]

        hour = fields[3]
        minute = fields[4]
        second = fields[5]
        millis = fields[6]

        tz_sign = fields[7]
        tz_hour = fields[8]
        tz_minute = fields[9]

        return cls(year, month, day, hour, minute, second, millis, tz_sign, tz_hour, tz_minute)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, year, month, day, hour, minute, second, millis, tz_sign, tz_hour, tz_minute):
        """
        Constructor
        """
        self.__year = year
        self.__month = month
        self.__day = day

        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__millis = millis

        self.__tz_sign = tz_sign
        self.__tz_hour = tz_hour
        self.__tz_minute = tz_minute


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def date(self):
        return "%s-%s-%s" % (self.year, self.month, self.day)


    @property
    def time(self):
        return "%s:%s" % (self.hour, self.minute)


    @property
    def time_secs(self):
        return "%s:%s:%s" % (self.hour, self.minute, self.second)


    @property
    def time_millis(self):
        return "%s:%s:%s.%s" % (self.hour, self.minute, self.second, self.millis)


    @property
    def timezone(self):
        return "%s%s:%s" % (self.tz_sign, self.tz_hour, self.tz_minute)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def year(self):
        return self.__year


    @property
    def month(self):
        return self.__month


    @property
    def day(self):
        return self.__day


    @property
    def hour(self):
        return self.__hour


    @property
    def minute(self):
        return self.__minute


    @property
    def second(self):
        return self.__second


    @property
    def millis(self):
        return self.__millis


    @property
    def tz_sign(self):
        return self.__tz_sign


    @property
    def tz_hour(self):
        return self.__tz_hour


    @property
    def tz_minute(self):
        return self.__tz_minute


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISO8601:{year:%s, month:%s, day:%s, hour:%s, minute:%s, second:%s, millis:%s, " \
               "tz_sign:%s, tz_hour:%s, tz_minute:%s}" % \
               (self.year, self.month, self.day, self.hour, self.minute, self.second, self.millis,
                self.tz_sign, self.tz_hour, self.tz_minute)
