import os
import sys
import json
import socket
import time
import jinja2

from .mailalert import EmailCore
from .logger import LoggerFactory
from .utils import spawnthread
from .log_fetcher import get_std_logs

logger = LoggerFactory.get_logger()


template_loc = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "email_templates")
hostname = socket.getfqdn()


def render(template, context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc)
    ).get_template(template).render(context)


from_addr = ""
to_addrlist = []
cc_addrlist = []
bcc_addrlist = []
envname = "unknown-environment"
smtp_host = ""
smtp_port = None
smtp_user, smtp_password, smtp_auth = None, None, None
timewindow = 5 * 60  # seconds
MAIL_RETRY_INTERVAL = 10  # seconds
TERMINAL_STATES = ('TASK_FAILED', 'TASK_KILLED', 'TASK_LOST', 'TASK_FINISHED')


def parse_conf(path):
    try:
        conf = json.load(open(path))
        global from_addr, to_addrlist, cc_addrlist, bcc_addrlist, smtp_host, smtp_port, smtp_user, smtp_password, smtp_auth
        global timewindow, envname
        from_addr = conf['email']['from']
        to_addrlist = conf['email']['to']
        cc_addrlist = conf['email']['cc']
        bcc_addrlist = conf['email']['bcc']
        timewindow = int(conf['timewindow'])
        envname = conf['envname']

        smtp_host = conf['smtp']['host']
        smtp_port = conf['smtp']['port']

        smtp_user = conf['smtp'].get('user')
        smtp_password = conf['smtp'].get('password')
        smtp_auth = conf['smtp'].get('auth')

    except Exception as e:
        logger.exception("Parsing configuration failed.")
        sys.exit(-2)


def alert_this_event(e):
    """
    event e =
    {
      "eventType": "status_update_event",
      "timestamp": "2014-03-01T23:29:30.158Z",
      "slaveId": "20140909-054127-177048842-5050-1494-0",
      "taskId": "my-app_0-1396592784349",
      "taskStatus": "TASK_RUNNING",
      "appId": "/my-app",
      "host": "slave-1234.acme.org",
      "ports": [31372],
      "version": "2014-04-04T06:26:23.051Z",
      "message": ""
    }

    subject example:   Failed: /infra/env/mysql (test_env)
    """
    subj_template = "[{envname}] marathon application {appid} - {status}:  "
    # ctime =  dt.utcnow().strftime('%c') + ' UTC'

    if e.taskStatus == 'TASK_LOST':
        title = 'Application was lost'
        status = 'Lost'
    elif e.taskStatus == 'TASK_FAILED':
        title = 'Application has failed'
        status = 'Failed'
    elif e.taskStatus == 'TASK_KILLED':
        title = 'Application was killed'
        status = 'Killed'
    elif e.taskStatus == 'TASK_FINISHED':
        title = 'Application has finished'
        status = 'Finished'
    else:
        status = e.taskStatus
        title = e.taskStatus

    subj = subj_template.format(status=status, appid=e.appId,
                                envname=envname)
    jinjacontext = {
        'marathonurl': "http://%s:8080/ui/#/apps%s" % (hostname, e.appId),
        'appid': e.appId,
        'message': e.message,
        "title": title,
        "timestamp": (e.timestamp).strftime('%d %b %Y %H:%M:%S UTC'),
        "appname": e.appId.split('/')[-1],
        "taskid": e.taskId,
        "node": e.host
    }

    # if e.taskStatus in ['TASK_LOST', 'TASK_FAILED']:
    app_host = e.host
    task_id = e.taskId
    logger.info('alerting failure of  %s at %s', task_id, app_host)
    logfiles = []
    try:
        stdout, stderr = get_std_logs(task_id, app_host)
        if stdout:
            logfiles.append(('stdout.txt', stdout))
        if stderr:
            logfiles.append(('stderr.txt', stderr))
    except Exception as oops:
        logger.exception("exception while fetching logs.")

    body = render('redalert.html', jinjacontext)
    send_mail_alert(subj, body, logfiles)


def alert_multiple(eventlist):
    subj_template = "[{envname}] marathon application is still failing : {appid}"
    appid = eventlist[0].appId
    subj = subj_template.format(appid=appid, envname=envname)
    jinjacontext = {
        'marathonurl': "http://%s:8080/ui/#/apps%s" % (hostname, appid),
        'title': "Appication has been failed multiple times",
        'appid': appid,
        'eventlist': eventlist,
        'TERMINAL_STATES': TERMINAL_STATES
    }

    # if e.taskStatus in ['TASK_LOST', 'TASK_FAILED']:
    body = render('multiple.html', jinjacontext)
    send_mail_alert(subj, body)


def alert_status(eventlist):
    if len(eventlist) == 1:
        alert_this_event(eventlist[0])
    else:
        alert_multiple(eventlist)


@spawnthread
def send_mail_alert(subj, body, attachments=[]):
    """
    eg: attachments = [('log.txt','hey this is a log file'), (filename, content)]
    """
    logger.info('preparing mail ..... attchement_count = %s', len(attachments))
    # with open('_mail.html','w') as f:
    #     f.write(body)
    ec = EmailCore()
    ec.set_mailheader(subject=subj, toaddrlist=to_addrlist, fromaddr=from_addr,
                      cclist=cc_addrlist, bcclist=bcc_addrlist)
    ec.set_recipients(to_addrlist)
    ec.prepare_html_body(body)
    for att in attachments:
        ec.attach_file_content(*att)

    try:
        trial_count = 0
        logger.info("sending mail to " + str(to_addrlist) + " via " + smtp_host + ":" + str(smtp_port))
        while trial_count < 10:
            try:
                trial_count += 1
                resp = ec.send(smtp_host, smtp_port, smtp_user, smtp_password, smtp_auth)
                logger.info('mail alert submitted successfully (total tries = %s , failed recipients: %s) '
                            % (trial_count, resp))
                return
            except Exception as oops:
                time.sleep(MAIL_RETRY_INTERVAL)
        # if here, mail was failed to submit after MAIL_RETRY_INTERVAL. reraise exception
        raise
    except Exception as oops:
        logger.exception("Error occured during sending mail alert (total tries = %s)" % trial_count)
        pass
