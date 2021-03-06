from  meas.core.marathonevents import *

sample_event =  """
                        {
                        "eventType": "status_update_event",
                        "timestamp": "2014-03-01T23:29:30.158Z",
                        "slaveId": "20140909-054127-177048842-5050-1494-0",
                        "taskId": "my-app_0-1396592784349",
                        "taskStatus": "TASK_FAILED",
                        "appId": "/my-app",
                        "host": "slave-1234.acme.org",
                        "ports": [31372],
                        "version": "2014-04-04T06:26:23.051Z"
                        }
                """


ef = EventFactory()
eventobj = ef.process(sample_event)

def test_EventFactory():
    assert eventobj.appId == "/my-app"
    assert eventobj.ports == [31372]
    print eventobj.stringify()
    print repr(eventobj)
    

if __name__ == '__main__':
    test_EventFactory()

