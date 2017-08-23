import SocketServer
import BaseHTTPServer

from .eventhandler import EventHandler
from .logger import LoggerFactory
logger = LoggerFactory.get_logger()


class AsyncHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """
    inherites from ThreadingMixIn to get asynchronous serving of requests
    """


class MeasServer(object):

    def __init__(self, host='0.0.0.0', port=7080, marathonlists=None):
        # TOOD: multiple marathon
        self.host = host
        self.port = port
        self._asyncServer = AsyncHTTPServer((self.host, self.port), EventHandler)

    def run_for_ever(self):
        logger.info('serving at {host}:{port}'.format(host=self.host, port=self.port))
        self._asyncServer.serve_forever()
        logger.warn('server stoped')


if __name__ == '__main__':
    pass
