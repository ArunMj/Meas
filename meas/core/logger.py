import traceback
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

class LOG(object):
    def __init__ (self, loggername, logfile):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        fileLogHandler = TimedRotatingFileHandler(logfile, 'midnight', 1, 31)
        fileLogHandler.setLevel(logging.DEBUG)
        logOutputFormat = logging.Formatter("%(asctime)-10s %(name)-10s %(levelname)-5s %(message)-30s")
        fileLogHandler.setFormatter(logOutputFormat)
        self.logger.addHandler(fileLogHandler)

    def info(self,p,*args):
        self.logger.info(p)
        sys.stdout.write(p + '\n')

    def debug(self,p,*args):
        self.logger.debug(p)
        sys.stdout.write(p + '\n')

    def warn(self,p,*args):
        self.logger.warn(p)
        sys.stdout.write(p + '\n')

    def error(self,p,*args):
        self.logger.exception(p)
        sys.stderr.write(p + '\n')
        traceback.print_exc()

log =  LOG('measlogger','measlog.log')

__all__ = [log]