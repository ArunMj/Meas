import json
from mailalert import EmailCore
import appstatusmonitor
from logger import log

from email_templates import ( app_failed_alert,
                              app_lost_alert,
                              multiple_termination_alert
                            )
from_addr = ""
to_addrlist = []
cc_addrlist = []
bcc_addrlist = []
subject_pefix = ""

smtp_host = ""
smtp_port = None

def parse_mail_conf(path):
    conf = json.load(open(path))
    global from_addr,to_addrlist,cc_addrlist,bcc_addrlist,subject_pefix,smtp_host,smtp_port
    from_addr = conf['email']['from']
    to_addrlist = conf['email']['to']
    cc_addrlist = conf['email']['cc']
    bcc_addrlist = conf['email']['bcc']
    subject_pefix = conf['email']['subject_pefix']

    smtp_host = conf['smtp']['host']
    smtp_port = conf['smtp']['port']


def alert_this_event(e):
    if e.taskStatus == 'TASK_LOST':
        body = app_lost_alert.getbody(e)
        subj = app_lost_alert.getsubject(e)
        send_mail_alert(subj,body)

    elif e.taskStatus == 'TASK_FAILED':
        body = app_failed_alert.getbody(e)
        subj = app_failed_alert.getsubject(e)
        send_mail_alert(subj,body)

def alert_this_app(appid):
    body = multiple_termination_alert.getbody(appid,appstatusmonitor.AppStatusRecorder)
    subj = multiple_termination_alert.getsubject(appid)
    if body is not None:
        send_mail_alert(subj,body)
        appstatusmonitor.AppStatusRecorder.delete_app_record(appid)

def send_mail_alert(subj,body):
    
    print 'preparing mail .....'
    # with open('mail.html','w') as f:
    #     f.write(body)
    subj = subject_pefix + '_' + subj
    ec = EmailCore()
    ec.set_mailheader(subject=subj,toaddrlist= to_addrlist,fromaddr=from_addr,
                                    cclist=cc_addrlist, bcclist=bcc_addrlist)
    ec.set_recipients(to_addrlist)
    ec.prepare_html_body(body)

    log.info("sending mail......")
    if  ec.send('postbud220.trv.flytxt.com',25):
        log.info('mail alert sent successfully')
    else:
        log.warn('mail alert failed.')

    
