"""
accounts events of type `MarathonStatusUpdateEvent`

"""

from collections import defaultdict
from marathonevents import MarathonStatusUpdateEvent
from datetime import datetime as dt,timedelta
import alertmanager
from email_templates import template
from logger import log

class AppStatusRecorder(object):
    
    # appid:eventlist
    event_bucket = defaultdict(list)
    
    TERMINAL_STATES = ('TASK_FAILED','TASK_KILLED','TASK_LOST')

    @classmethod
    def add_event(cls,event):

        """
        Accepts MarathonStatusUpdateEvent and triggers alert, stores event histories
        """
        log.debug("added to record : "+repr(event))
        app_id = event.appId
        event_time = event.timestamp

        cls.event_bucket[app_id].append(event)

        alertmanager.alert_this_event(event)
        if event.taskStatus in cls.TERMINAL_STATES:
            alertmanager.alert_this_app(app_id)

        # print "ALL", cls.get_events_in_last_xseconds(app_id,lastxseconds = 40)
        # print "TERM", cls.get_events_in_last_xseconds(app_id,lastxseconds = 40,
        #                             filter_predicate=lambda e: e.taskStatus in cls.TERMINAL_STATES)

        
    # @classmethod
    # def alert_app_status(cls,appid):
    #     if not cls.event_bucket.has_key(appid):
    #         return
    #     eventlist = cls.event_bucket[appid]
    #     print "$$$$"
    #     count = cls.get_rate_of_failure(eventlist)
    #     print "RATE",count
    #     if count > 4:
    #         print "sends alert for ",appid
    #         send_alert(appid,eventlist)
    #         print "deletes eventlist of ",appid
    #         del eventlist[:]

    @classmethod
    def delete_app_record(cls,appid):
        cls.event_bucket.pop(appid,None)

    @classmethod
    def get_events_in_last_xseconds(cls,appid,lastxseconds=300,filter_predicate=None):
        
        now = dt.utcnow()
        from_time = now - timedelta(seconds=lastxseconds)

        eventlist = []
        all_events = cls.event_bucket[appid]
        #print eventlist
        for e in all_events:
            if e.timestamp >= from_time:
                if filter_predicate and not filter_predicate(e): # applies filter if mensioned
                    continue  # this wont match for filter case; so skipp it
                eventlist.append(e)
        return eventlist


        

