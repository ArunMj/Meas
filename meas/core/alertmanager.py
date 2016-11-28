import json
from mailalert import EmailCore

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

"""
    get_mail_body(
                subject_prefix,app_id,marathon_host,time
            )
"""

def send_mail_alert():
    body = template.getbody(appid,eventlist)
    subj = template.getsubject(appid)
    # print subj
    print 'writing body.....'
    with open('mail.html','w') as f:
        f.write(body)

    log.info("sending mail......")
    ec = EmailCore()
    ec.set_mailheader(subject=subj,toaddrlist= to_addrlist,fromaddr=from_addr)
    ec.set_recipients(to_addrlist)
    ec.prepare_html_body(body)

    if  ec.send('postbud220.trv.flytxt.com',25):
        log.info('mail alert sent successfully')
    else:
        log.error('mail alert failed.')

    
