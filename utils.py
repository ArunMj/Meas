from datetime import datetime as dt

def conv_datestring(datestr):
    return dt.strptime(datestr,'%Y-%m-%dT%H:%M:%S.%fZ')