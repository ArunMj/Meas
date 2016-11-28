"""
accounts events of type `MarathonStatusUpdateEvent`

"""

from collections import defaultdict
from marathonevents import MarathonStatusUpdateEvent
from datetime import datetime as dt,timedelta as td

from email_templates import template


def send_alert(appid,eventlist):
    body = template.getbody(appid,eventlist)
    subj = template.getsubject(appid)
    # print subj
    # print 'writing body.....'
    with open('mail.html','w') as f:
        f.write(body)
    print "sending mail......"
    ec = EmailCore()
    ec.set_mailheader(subject=subj,toaddrlist='mjhack08@gmail.com',fromaddr='marathon-alert@flytxt.com')
    ec.set_recipients(['mjhack08@gmail.com'])
    ec.prepare_html_body(body)
    print ("success" if  ec.send('postbud220.trv.flytxt.com',25) else "failed")


class AppStatusRecorder(object):
    
    # appid:eventlist
    critical_event_bucket = defaultdict(list)
    
    TERMINAL_STATES = ('TASK_FAILED','TASK_KILLED','TASK_LOST')

    @classmethod
    def add_event(cls,event):

        """
        Accepts MarathonStatusUpdateEvent
        """

        if event.taskStatus not in cls.TERMINAL_STATES:
            return

        app_id = event.appId
        event_time = event.timestamp
        cls.critical_event_bucket[app_id].append(event)
        cls.alert_app_status(app_id)
        
    @classmethod
    def alert_app_status(cls,appid):
        if not cls.critical_event_bucket.has_key(appid):
            return
        eventlist = cls.critical_event_bucket[appid]
        print "$$$$"
        count = cls.get_rate_of_failure(eventlist)
        print "RATE",count
        if count > 4:
            print "sends alert for ",appid
            send_alert(appid,eventlist)
            print "deletes eventlist of ",appid
            del eventlist[:]

    @classmethod
    def delete_app_record(cls,appid):
        cls.critical_event_bucket.pop(appid,None)

    @staticmethod
    def get_rate_of_failure(eventlist,lastxseconds=300):
        rate = 0
        now = dt.utcnow()
        from_time = now- td(seconds=lastxseconds)
        print now,from_time
        #print eventlist
        for e in eventlist:
            print repr(e.timestamp)
            if e.timestamp >= from_time:
                rate+=1
        return rate


        

