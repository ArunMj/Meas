from datetime import datetime as dt
from os import path
import threading


def conv_datestring(datestr):
    return dt.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%fZ')


def getconfdir():
    loc = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'conf')
    if not path.exists(loc):
        raise Exception('conf directory note found')
    return loc


def pathjoin(a, b):
    return path.join(a, b)


def spawnthread(f):
    def func(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return func


if __name__ == '__main__':
    # test
    d = conv_datestring("2014-04-04T06:26:23.051Z")
    assert repr(d) == "datetime.datetime(2014, 4, 4, 6, 26, 23, 51000)"
