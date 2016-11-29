from marathonevents import EventFactory,MarathonStatusUpdateEvent
from logger import log
import BaseHTTPServer
import time
from appstatusmonitor import AppStatusRecorder
event_factory = EventFactory()

class EventHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("status", 'not implimented')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data =  self.rfile.read(content_length)
        event = event_factory.process(data)

        if  isinstance(event,MarathonStatusUpdateEvent):
            AppStatusRecorder.add_event(event)

        # elif:  add here other event flows
        #  ..............

        else:
            # some events are unhandled.
            log.debug('unaccounted event : ' + repr(event))


        self.send_response(201)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('{"notify": "success""}')
        return

    def log_request(self, code='-', size='-'):
        #self.log_message('"%s" %s %s',self.requestline, str(code), str(size))
        pass 