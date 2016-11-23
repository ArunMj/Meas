import json
from logger import log

from utils import conv_datestring

class MarathonEventBase(object):
    """
    """

    KNOWN_ATTRIBUTES = []

    def __init__(self, eventType, timestamp, **kwargs):
        """
            accepts json event representation, 
            `eventType` and `timestamp` are always present keys
        """
        self.event_type = eventType  # All events have these two attributes
        self.timestamp = conv_datestring(timestamp)
        
        for attribute_name in self.KNOWN_ATTRIBUTES:
            attribute = kwargs.get(attribute_name,None)
            setattr(self, attribute_name, attribute)

    def stringify(self):
        return str(self)

    def __str__(self):
        tstring = "[{type} @ {time}]\n\t{attr}"
        attrstring = '\n\t'.join([attribute + " : " + str(getattr(self, attribute)) 
                                    for attribute in self.KNOWN_ATTRIBUTES]
                     )
        return tstring.format(type=self.event_type.upper(),
                              time=self.timestamp.strftime("%d-%m-%y %H:%M:%S.%f UTC"),
                              attr=attrstring)
    
    

class MarathonApiPostEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['clientIp', 'appDefinition', 'uri']


class MarathonStatusUpdateEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = [
        'slaveId', 'taskId', 'taskStatus', 'appId', 'host', 'ports', 'version', 'message']


class MarathonFrameworkMessageEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['slaveId', 'executorId', 'message']


class MarathonSubscribeEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['clientIp', 'callbackUrl']


class MarathonUnsubscribeEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['clientIp', 'callbackUrl']


class MarathonAddHealthCheckEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId', 'healthCheck', 'version']


class MarathonRemoveHealthCheckEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId', 'healthCheck']


class MarathonFailedHealthCheckEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId', 'healthCheck', 'taskId']


class MarathonHealthStatusChangedEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId', 'healthCheck', 'taskId', 'alive']


class MarathonGroupChangeSuccess(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['groupId', 'version']


class MarathonGroupChangeFailed(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['groupId', 'version', 'reason']


class MarathonDeploymentSuccess(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['id']


class MarathonDeploymentFailed(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['id']


class MarathonDeploymentInfo(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonDeploymentStepSuccess(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonDeploymentStepFailure(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonEventStreamAttached(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['remoteAddress']


class MarathonEventStreamDetached(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['remoteAddress']


class MarathonUnhealthyTaskKillEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId', 'taskId', 'version', 'reason']

class MarathonAppTerminatedEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['appId']

class MarathonSchedulerRegisteredEvent(MarathonEventBase):
    KNOWN_ATTRIBUTES = ['master','frameworkId']


class EventFactory:
    """
    """

    def __init__(self):
        pass

    event_to_class = {
        'api_post_event': MarathonApiPostEvent,
        'status_update_event': MarathonStatusUpdateEvent,
        'framework_message_event': MarathonFrameworkMessageEvent,
        'subscribe_event': MarathonSubscribeEvent,
        'unsubscribe_event': MarathonUnsubscribeEvent,
        'add_healthCheck_event': MarathonAddHealthCheckEvent,
        'remove_healthCheck_event': MarathonRemoveHealthCheckEvent,
        'failed_healthCheck_event': MarathonFailedHealthCheckEvent,
        'health_status_changed_event': MarathonHealthStatusChangedEvent,
        'unhealthy_task_kill_event': MarathonUnhealthyTaskKillEvent,
        'group_change_success': MarathonGroupChangeSuccess,
        'group_change_failed': MarathonGroupChangeFailed,
        'deployment_success': MarathonDeploymentSuccess,
        'deployment_failed': MarathonDeploymentFailed,
        'deployment_info': MarathonDeploymentInfo,
        'deployment_step_success': MarathonDeploymentStepSuccess,
        'deployment_step_failure': MarathonDeploymentStepFailure,
        'event_stream_attached': MarathonEventStreamAttached,
        'event_stream_detached': MarathonEventStreamDetached,
        'scheduler_registered_event':MarathonSchedulerRegisteredEvent,
        'app_terminated_event': MarathonAppTerminatedEvent
    }

    def process(self, event_json_str):
        try:
            event_json = json.loads(event_json_str)
            event_type = event_json['eventType']
            if event_type in self.event_to_class:
                eventclass = self.event_to_class[event_type]
                return eventclass(**event_json)
            else:
                raise Exception('Unknown event_type: {}, data: {}'.format(event_type, event_json))
        except Exception as oops:
            log.error("Could not process event data",oops)