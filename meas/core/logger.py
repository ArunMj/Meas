import logging
from logging.handlers import TimedRotatingFileHandler

class LoggerFactory(object):
    _logger = None

    @classmethod
    def init(cls, logfile, loggername='measlogger', level=logging.INFO):
        if cls._logger:
            return
        cls._logger = logging.getLogger(loggername)
        cls._logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)-10s %(name)-10s [%(threadName)s] %(levelname)-5s %(message)-30s")

        fileLogHandler = TimedRotatingFileHandler(logfile, 'midnight', 1, 31)
        fileLogHandler.setLevel(level)
        fileLogHandler.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        cls._logger.addHandler(ch)
        cls._logger.addHandler(fileLogHandler)

    @classmethod
    def get_logger(cls):
        if not cls._logger:
            raise("logger not initialized")
        return cls._logger