from datetime import datetime as dt

def conv_datestring(datestr):
    return dt.strptime(datestr,'%Y-%m-%dT%H:%M:%S.%fZ')



if __name__ == '__main__':
    d = conv_datestring("2014-04-04T06:26:23.051Z")
    assert repr(d) == "datetime.datetime(2014, 4, 4, 6, 26, 23, 51000)"