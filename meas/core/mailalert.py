import mimetypes
import os
import re
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class MailException(Exception):
    pass


class EmailCore(object):

    def __init__(self):
        self.mail = MIMEMultipart()
        self._isheaderOK = False
        self.recipients_list = None

    def set_mailheader(self, subject, fromaddr, toaddrlist, cclist=[], bcclist=[]):

        self.mail['Subject'] = subject
        self.mail['To'] = ','.join(self._makelist(toaddrlist))
        self.mail['From'] = fromaddr
        self.mail['CC'] = ','.join(self._makelist(cclist))
        self.mail['BCC'] = ','.join(self._makelist(bcclist))
        self.mail.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        self._isheaderOK = True
        # print self. mail

    def set_recipients(self, recipients_list):
        if len(recipients_list) == 0:
            raise MailException(
                "recipients_list should not be empty.")
        self.recipients_list = recipients_list

    def prepare_text_body(self, text):
        _text_mime = MIMEText(text, 'plain')
        if self.mail:
            self.mail.attach(_text_mime)

    def prepare_html_body(self, html_template):
        _html_mime = MIMEText(html_template, 'html')
        if self.mail:
            self.mail.attach(_html_mime)

    def attach_file_content(self, filename, data):
        part = MIMEApplication(data, Name=filename)
        part['Content-Disposition'] = 'attachment; filename="%s"' % filename
        self.mail.attach(part)

    def send(self, host, port, user=None, password=None, auth=None):
        if not self.recipients_list:
            raise MailException(
                "No recipients details has set.")

        if not self._isheaderOK:
            raise Exception(
                "No mail-header details has set.")
        frm = self.mail['From']
        # print 'from',frm

        if auth == 'tls':
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
        elif auth == 'ssl':
            server = smtplib.SMTP_SSL(host, port)
            server.ehlo()
        elif auth:
            # TODO:
            raise NotImplementedError
        else:
            server = smtplib.SMTP(host, port)
            # print server.ehlo()

        if user or password:
            print server.login(user, password)

        resp = server.sendmail(
            frm,
            self.recipients_list,
            self.mail.as_string()
        )
        server.quit()

        # resp is {} if all recipients are accepted.
        # This method will return normally if the mail is accepted for at least
        # one recipient.  It returns a dictionary, with one entry for each
        # recipient that was refused.
        return resp

    def _makelist(self, addr):
        if isinstance(addr, str):
            return (addr,)
        else:
            return iter(addr)


class MailAlert(EmailCore):
    pass


if __name__ == '__main__':
    # TEST
    #
    ec = EmailCore()
    ec.set_mailheader(subject='test', toaddrlist='arun.muraleedharan@flytxt.com', fromaddr='noreplay@marathon.alert')
    ec.set_recipients(['arun.muraleedharan@flytxt.com', 'wsexyvkm@sharklasers.com', 'arunmj123@yahoo.com'])
    with open('core/_mail.html') as f:
        body = f.read()
    ec.prepare_html_body(body)
    print ec.send('postbud220.trv.flytxt.com', 25)
    print "ok"
