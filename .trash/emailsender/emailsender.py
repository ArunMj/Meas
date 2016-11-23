import mimetypes
import os
import re
import smtplib

from email import encoders
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class EmailCore:
    '''This class contains method for sending
    emails with/without attachments'''
    
    MAIL_REG_EXP_COMPILE = re.compile(
        r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$')
    
    def __init__(self):
        self.invalid_ids = None
        self.text_mime = None
        self.html_mime = None
        self.attach_mime = None
        self.recipients = None
        self.mail = None
        self.frm = None
        
        
    def set_mailheader(self, args):
        subject = args.get('subject', None)
        to = args.get('to', None)
        frm = args.get('from', None)
        cc = args.get('cc', ())
        bcc = args.get('bcc', ())
        print frm
        if subject and to and frm:
            self._prepare_email(subject, to, cc, frm, bcc)
        else:
            raise Exception(
                """Sorry, We can't prepare the mail header 
                    as it misses the important fields""")
                    
    def set_high_priority(self):
        if self.mail:
            self.mail['X-Priority'] = '1'
            self.mail['X-MSMail-Priority'] = 'High'
        
    def prepare_text_body(self, text):
        self.text_mime = MIMEText(text, 'plain')
        if self.mail:
			self.mail.attach(self.text_mime)

    def prepare_html_body(self, html_template):
        self.html_mime = MIMEText(html_template, 'html')
        if self.mail:
			self.mail.attach(self.html_mime)
        
    def set_recipients(self, recipients):
        if len(recipients) == 0:
            raise Exception(
                    "Sorry, Recipients list is empty.")
        
        self.recipients = recipients
        self.invalid_ids = self._validate_all_emailids()
                
    def _prepare_email(self, subject, to, frm, bcc,cc):
        mail = MIMEMultipart()
        mail['Subject'] = subject
        mail['To'] = ','.join(to)
        mail['From'] = frm
        mail['CC'] = ','.join(cc)
        mail['BCC'] = ','.join(bcc)
        mail.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        print mail
        self.mail = mail
        

    def send(self, host, port, priorty=None):
        success = False
        err = ''
        if not self.recipients:
            raise Exception(
                "Sorry, You dont set the recipients details")
                    
        if not self.mail:
            raise Exception(
                    "Sorry, You don't set the mail header")

        try:
            s = smtplib.SMTP(host, port)
            s.sendmail(
                self.frm,
                self.recipients,
                #self.mail.as_string()
                "fjsgdjhfgsj"
                )
            s.quit()
            success = True
        except Exception, e:
            err = e
        
        return (success, err) 

    def hook_attachment(self, file_path, attach_name=None):
        
        ctype, encoding = mimetypes.guess_type(
                    self._check_file_validity(file_path))
        if not ctype:
            ctype = 'application/ms-excel'
        maintype, subtype = ctype.split('/', 1)
        
        fp = open(file_path, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()

        encoders.encode_base64(msg)
        
        if not attach_name:
            attach_name = os.path.basename(file_path)
        msg.add_header('Content-Disposition',
                       'attachment',
                       filename=attach_name)
        self.attach_mime = msg
        
        if self.mail:
			self.mail.attach(self.attach_mime)
        
    def get_invalid_emailids(self):
        return self.invalid_ids

    def _validate_all_emailids(self):
        invalid_ids = []
        for mail_id in self.recipients:
            if not self._validate_email(mail_id):
                invalid_ids.append(mail_id)
                
        return invalid_ids

    def _validate_email(self, email_id):
        valid = True
        if not self.MAIL_REG_EXP_COMPILE.match(email_id.strip()):
            valid = False

        return valid
        
    def _check_file_validity(self, name):
        '''Returns the file name if it has a valid path'''
        abs_path = validate_file(name)
        if not abs_path:
            raise FlyTxtXMLError(
               "File you wish to attach to the mail '%s' doesn't exist." % name)
        return abs_path
    


ec = EmailCore()
ec.set_mailheader({'subject':'test', 'to':['x@y.com'],'from':'noreplay@y.com'})
ec.set_recipients(['arun.muraleedharan@flytxt.com'])
ec.prepare_text_body("hello world")
(a,b) = ec.send('postbud220.trv.flytxt.com',25)
print a,b