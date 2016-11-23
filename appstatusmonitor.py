from  collections import defaultdict
from marathonevents import MarathonStatusUpdateEvent



def send_alert(appid,eventlist):
    t =''
    for events in eventlist:
        t += '\t'+str(events.timestamp)+'\n'

    print t

class AppStatusRecorder(object):
    
    # appid:eventlist
    critical_event_bucket = defaultdict(list)
    
    TERMINAL_STATES = ('TASK_FAILED','TASK_KILLED','TASK_LOST')

    @classmethod
    def add_event(cls,event):
        """
        Accepts MarathonStatusUpdateEvent
        """
        if not isinstance(event,MarathonStatusUpdateEvent):
            return

        if event.taskStatus not in cls.TERMINAL_STATES:
            print event.taskStatus
            return
        print "bad"
        app_id = event.appId
        event_time = event.timestamp
        cls.critical_event_bucket[app_id].append(event)
        cls.check_app_health(app_id,4)
        
    @classmethod
    def check_app_health(cls,appid,level):
        
        if not  cls.critical_event_bucket.has_key(appid):
            return
        eventlist = cls.critical_event_bucket[appid]

        if len(eventlist) > 4:
            print "sends alert for ",appid
            send_alert(appid,eventlist)
            print "deletes eventlist of ",appid
            del eventlist[:]
        



    @classmethod
    def delete_app_record(cls,appid):
        cls.critical_event_bucket.pop(appid,None)
        

