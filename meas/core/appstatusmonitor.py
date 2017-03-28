"""
accounts events of type `MarathonStatusUpdateEvent`

"""

from collections import defaultdict
from marathonevents import MarathonStatusUpdateEvent
from datetime import datetime as dt,timedelta
import alertmanager
from logger import log

class AppStatusRecorder(object):
    
    # appid:eventlist
    event_bucket = defaultdict(list)
    
    TERMINAL_STATES = ('TASK_FAILED','TASK_KILLED','TASK_LOST','TASK_FINISHED')

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

    @classmethod
    def delete_app_record(cls,appid):
        cls.event_bucket.pop(appid,None)

    @classmethod
    def get_events_in_last_xseconds(cls,appid,lastxseconds=300,filter_predicate=None):
        
        now = dt.utcnow()
        #print now
        from_time = now - timedelta(seconds=lastxseconds)

        eventlist = []
        all_events = cls.event_bucket[appid]
        #print eventlist
        for e in all_events:
            if e.timestamp >= from_time:
                if filter_predicate and not filter_predicate(e): # applies filter if mensioned
                    continue  # this wont match for filter case; so skipp it
                eventlist.append(e)
        #print eventlist
        return eventlist


        

