import BaseHTTPServer

from .marathonevents import EventFactory, MarathonStatusUpdateEvent
from .appstatusmonitor import AppStatusRecorder
from .logger import LoggerFactory


logger = LoggerFactory.get_logger()
event_factory = EventFactory()


class EventHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("status", 'not implimented')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        event = event_factory.process(data)

        if event is None:
            logger.warn("invalid event data received")

        if isinstance(event, MarathonStatusUpdateEvent):
            logger.debug("STATUS:" + event.tojson())
            AppStatusRecorder.add_event(event)

        # elif:  add here other event flows
        #  ..............

        else:
            # some events are unhandled.
            logger.warn('unaccounted event : ' + repr(event))

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"notify": "success"}')
        return

    def log_request(self, code='-', size='-'):
        #self.log_message('"%s" %s %s',self.requestline, str(code), str(size))
        pass
