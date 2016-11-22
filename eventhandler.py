from marathonevents import *
from logger import log
import BaseHTTPServer
import time
event_factory = EventFactory()

class EventHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("status", 'not implimented')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data =  self.rfile.read(content_length)
        event = event_factory.process(data)
        if event:
            log.info("event post recieved\n"  + event.stringify())
        self.send_response(201)