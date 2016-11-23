from marathonevents import *
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
        #print self.headers
        # if event : #and hasattr(event,'version'):
        #     log.info("event post recieved\n"  + event.stringify())
        AppStatusRecorder.add_event(event)
        self.send_response(201)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('{"notify": "success""}')
        return
