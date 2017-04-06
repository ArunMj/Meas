import traceback
import sys
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import threading

class LOG(object):
    def __init__ (self, loggername, logfile):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.INFO)
        fileLogHandler = TimedRotatingFileHandler(logfile, 'midnight', 1, 31)
        fileLogHandler.setLevel(logging.INFO)
        logOutputFormat = logging.Formatter("%(asctime)-10s %(name)-10s %(levelname)-5s %(message)-30s")
        fileLogHandler.setFormatter(logOutputFormat)
        self.logger.addHandler(fileLogHandler)

    def info(self,p,*args):
        self.logger.info(p)
        sys.stdout.write(p + '\n')

    def debug(self,p,*args):
        self.logger.debug(p)
        sys.stdout.write( "****["+threading.current_thread().getName()+"] ---- "+p + '\n')

    def warn(self,p,*args):
        self.logger.warn(p)
        sys.stdout.write(p + '\n')

    def error(self,p,*args):
        self.logger.exception(p)
        sys.stderr.write(p + '\n')
        traceback.print_exc()

log =  None

def set_logger(filepath):
    try:
        global log
        log =  LOG('measlogger',filepath)
        print "logs will be saved in " + filepath
    except Exception as oops:
        print 'logger',oops,'deafult log file <meas.log> will be used'
        log =  LOG('measlogger','meas.log')

__all__ = [log]
