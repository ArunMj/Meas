"""
accounts events of type `MarathonStatusUpdateEvent`

"""

from collections import defaultdict
from marathonevents import MarathonStatusUpdateEvent
from datetime import datetime as dt,timedelta
import alertmanager
from alertmanager import TERMINAL_STATES
from logger import log

class AppStatusRecorder(object):

    # appid:eventlist
    event_bucket = defaultdict(list)
    alerthistory = dict()

    @classmethod
    def add_event(cls,event):

        """
        Accepts MarathonStatusUpdateEvent and triggers alert, stores event histories
        """
        app_id = event.appId
        event_time = event.timestamp
        cls.event_bucket[app_id].append(event)
        log.debug("added to record : "+repr(event) +" - " + event.taskStatus)

        if event.taskStatus in TERMINAL_STATES:
            last_alert_time = cls.alerthistory.get(app_id, None)
            eventlist = []
            if not last_alert_time:
                #first time terminal event happend for this appId
                log.debug("toast to first failure!!")
                eventlist = [event]
            else:
                idle_time = (dt.utcnow() - last_alert_time).total_seconds()
                log.debug( "idle_time = "+ str(idle_time))
                if idle_time < alertmanager.timewindow:
                    # next alert is only after exeeding time window
                    log.debug("which is less than " + str(alertmanager.timewindow))
                    return

                # gets all Failure in last idletime
                failures = cls.get_events_in_last_xseconds(app_id,
                    lastxseconds=idle_time,
                    filter_predicate = lambda e: e.taskStatus in TERMINAL_STATES)
                log.debug("failures " +str(failures))
                if not failures:
                    # no failures in last idle time
                    return
                elif len(failures) == 1:
                    #single  failure after a long time
                    eventlist = failures
                elif len(failures) > 1:
                    #multiple failures. so gets all history
                    eventlist = cls.get_events_in_last_xseconds(app_id,
                                    lastxseconds=idle_time)
            if eventlist:
                log.debug( "events to alert ### " +str(eventlist))
                cls.reset_record(app_id)
                alertmanager.alert_status(eventlist)


    @classmethod
    def reset_record(cls,appid):
        cls.event_bucket.pop(appid,None)
        cls.alerthistory[appid] = dt.utcnow()

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
