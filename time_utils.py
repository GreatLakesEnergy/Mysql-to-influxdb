from datetime import datetime,timedelta
from dateutil.parser import parse
from time import localtime,strftime
from django.conf import settings
from  pytz import timezone
from django.utils import timezone as timezone_dt
from tzwhere import tzwhere


def get_epoch(tz=None):
    """
    Return number of seconds since 1970-01-01- epoch
    """
    now = datetime.now()
    if tz:
        tz = _clean_tz(tz)
        now = timezone_dt.now(tz)
    epoch = datetime(1970,1,1)
    diff = now - epoch
    diff = str(diff.total_seconds())
    diff_seconds = diff.split('.')
    diff_int = diff_seconds[0]
    return diff_int

def get_yesterday(tz=None):

    now = datetime.date(datetime.now())
    if tz:
        tz = _clean_tz(tz)
        now = timezone_dt.now(tz)

    one_day = timedelta(days=1)
    return now - one_day


def get_time_interval_array(interval,interval_type,start,end,tz=None):
    """
    Get an array between the provided time frame
    with slices in the given interval timedelta
    between start and end
    """

    if tz:
        tz = _clean_tz(tz)
        timez = timezone(tz)
    else:
        timez = timezone(settings.TIME_ZONE)
    # TODO finish timezone implemenation
    result = []
    kwargs = {}
    kwargs[interval_type] = interval
    interval = timedelta(**kwargs)
    while start < end:
        start = start + interval
        result.append(start)

    return result

def get_epoch_from_datetime(date):
    """
    Return number of seconds since 1970-01-01- epoch
    from given date
    @params: dateobject
    """
    epoch =  datetime(1970,1,1)
    if date.tzinfo:
        epoch = datetime(1970,1,1,tzinfo=date.tzinfo)
    diff = date - epoch
    seconds_only = str(diff.total_seconds())
    seconds_only_str = seconds_only.split('.')
    seconds_only = seconds_only_str[0]
    return seconds_only

def get_epoch_from_date(year, month, day, hours, minutes, tz=None):
    """
    Return number of seconds since 1970-01-01- epoch
    from given date
    @params: month,day,year,hours,minutes
    """
    date = datetime(year,month,day,hours,minutes)
    if tz:
        tz = _clean_tz(tz)
        date = datetime(year,month,day,hours,minutes,tzinfo=tz)

    epoch = datetime(1970,1,1)
    diff = date - epoch
    return diff.total_seconds()

def localize(nv_datetime,tz):
    """
    Add timezone info to datetime object
    """
    if not isinstance(nv_datetime,datetime):
        try:
            # Try to convert to datetime
            time = datetime(nv_datetime)
        except Exception, e:
            return nv_datetime
    # Is our datetime object  naive?
    if nv_datetime.tzinfo is not None and nv_datetime.tzinfo.utcoffset(nv_datetime) is not None:
        return nv_datetime
    localtz = timezone(tz)
    dt_aware = localtz.localize(nv_datetime)
    return dt_aware


def epoch_to_date(seconds_time, tz=None):
    """
    Translate seconds time to date
    """
    time = strftime('%Y-%m-%d',localtime(seconds_time))
    if tz:
        tz = _clean_tz(tz)
        time = localize(time,tz)

    return time

def get_timezone_from_geo(lat, lon):
    """
    Return String TimeZone from provided lat,lon
    """
    tz = tzwhere.tzwhere()
    return tz.tzNameAt(float(lat), float(lon))

def epoch_to_datetime(seconds_time, tz=None):
    """
    Translate seconds time to datetime object
    """
    time = datetime.fromtimestamp(seconds_time)

    if tz:
        tz = _clean_tz(tz)
        time = localize(time,tz)


    #return strftime('%Y-%m-%dT%XZ',time)
    return time


def get_last_five_days(from_date="now", tz=None):
    """
    Get last days returned to you as datetime objects in array
    @params:
        from_date: (date to return consecutive days ongoing from) (optional)
    """
    days = []

    now = datetime.now()
    if not from_date == "now":
        now = timezone.now()

    if not from_date == "now":
        now = from_date

    delta = now - timedelta(5)
    for day in xrange(1,6):
        days.append(delta)
        delta = delta + timedelta(1)
    return days


def get_days_interval_delta(start, end, delta=1):

    """
    return the days inbetween the two sepcified dates
    @params:
    start: when is the interval stardate, datetime object
    end: when should the interval end , datatime object
    delta: increments in which to return dates, integer, default 1 day
    """
    delta =  timedelta(days=delta)
    curr = start
    days  = []
    while curr < end:
        days.append(curr)
        curr += delta
    return days

def get_start_end_date(days_ago, start_day):
    """
    get the delta of days ago from given start date
    """
    delta = start_day - timedelta(days=days_ago)
    return delta

def get_timesince_seconds(time, tz=None):
    """
    Get timesince and time provided
    """
    now = timezone_dt.now()
    if tz:
        now = timezone(tz).localize(datetime.now())

    #loc = timezone(settings.TIME_ZONE)
    #now = loc.localize(now)
    diff =  now - time
    return int(diff.total_seconds())

def get_timesince(time, tz=None):

    now = datetime.now()
    if tz:
        tz = _clean_tz(tz)
        now = timezone_dt.now(tz)

    loc = timezone(settings.TIME_ZONE)
    now = loc.localize(now)
    diff =  now - time
    diff = format_timesince_seconds(int(diff.total_seconds()))
    return diff

def format_timesince_seconds(seconds):
    seconds = abs(seconds)
    if seconds < 60:
        if seconds == 1:
            return seconds, " second ago"
        else:
            return seconds, " seconds ago"
    elif seconds < 3600:
        if seconds/60 < 2: # if it is still a minute
            return seconds/60, " minute ago"
        else:
            return seconds/60, " minutes ago"
    elif seconds < 86400:
        if seconds/3600 < 2:
            return seconds/3600, " hour ago"
        else:
            return seconds/3600, " hours ago"

    else:
        if seconds/86400 < 2:
            return seconds/86400, " day ago"
        else:
            return seconds/86400, " days ago"
    

def get_date_dashed(date):
    date_string = str(date.year) + '-' + str(date.month) +  '-' + str(date.day)
    return date_string


def convert_influx_time_string(date_string, tz=None):
    """ Converts influx style strings to datetime """
    parsed = parse(date_string)

    if tz:
        parsed =parsed.astimezone(timezone(tz))

    return parsed

def get_timesince_influx(date_string):
    date_obj = convert_influx_time_string(date_string)
    return get_timesince(date_obj)

def _clean_tz(tz):
    return tz.strip().replace('\'','').replace('\"','')
